from odoo import fields, models, api


class Subcapitulo(models.Model):
    _name = "sub.capitulo"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    ###### DATOS PRINCIPALES  ########
    number = fields.Char(
        string="Number",
        required=True,
        copy=False,
        readonly="True",
        default=lambda self: self.env["ir.sequence"].next_by_code(
            "secuencia.subcapitulo"
        ),
    )
    numero_subcapitulo = fields.Char(string="Número Subcapítulo", required=False)
    name = fields.Char(string="Subcapítulo", required=True)
    descripcion = fields.Text("Descripción del Subcapítulo")
    cantidad = fields.Integer("Cantidad")
    fecha_inicio = fields.Date("Fecha Inicio")
    fecha_finalizacion = fields.Date("Acaba el")

    total = fields.Float("Importe Total", compute="_compute_total_sub")
    total_prevision = fields.Float("Importe Total Previsto")

    condicion = fields.Selection(
        string="Condición",
        selection=[
            ("presupuestario", "Presupuestario"),
            ("sobrecoste", "Sobre Coste"),
            ("adicionales", "Adicionales"),
        ],
        required=False,
    )

    ###### FASES DEL PROYECTO  ########
    project_id = fields.Many2one("project.project", string="Proyecto", required=True)
    capitulo_id = fields.Many2one(
        "capitulo.capitulo", string="Capitulo", ondelete="cascade", required=True
    )
    fase_principal_id = fields.Many2one(
        comodel_name="fase.principal", string="Fase Principal", required=True
    )
    # fase_principal_id = fields.Many2one(related='capitulo_id.fase_principal_id', string='Fase Principal', required=False)
    subcapitulo_ids = fields.One2many(
        comodel_name="item.capitulo",
        inverse_name="subcapitulo_id",
        string="Subcapitulo",
        required=False,
    )
    partidas_ids = fields.One2many(
        comodel_name="partidas.partidas",
        inverse_name="subcapitulo_id",
        string="Partidas id",
        required=False,
    )

    ###### CONTADORES  ########
    partidas_count = fields.Integer(
        string="Contador Item", compute="get_partidas_count"
    )
    activ_count = fields.Integer(
        string="Contador actividades", compute="get_acts_count"
    )

    estado = fields.Selection(
        string="Estado",
        selection=[
            ("borrador", "Borrador"),
            ("aprobada", "Aprobada en Prevision"),
            ("aprobadaproceso", "Aprobada en Proceso"),
            ("pendiente", "Pendiente Validar"),
            ("noaprobada", "No aprobada"),
        ],
        required=False,
        default="borrador",
    )

    @api.onchange("number", "capitulo_id")
    def _onchange_join_number(self):
        self.numero_subcapitulo = (
            str(self.capitulo_id.numero_capitulo) + "." + str(self.number)
        )

    labor_total = fields.Float(string="Total Coste Mano de Obra", readonly="True")
    machinerycost_total = fields.Float(string="Total Coste Maquinaria", readonly="True")
    overhead_total = fields.Float(string="Total Costes Generales", readonly="True")
    jobcost_total = fields.Float(string="Total Coste", readonly="True")

    # Calculos
    @api.depends("item_capitulo_materiales_ids")
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = material_total = 0.0
            for line in order.item_capitulo_materiales_ids:
                # amount_untaxed += 1
                # amount_untaxed += line.price_subtotal
                material_total += line.total_item_capitulo
            order.update(
                {
                    # 'amount_untaxed': amount_untaxed,
                    "material_total": material_total,
                    # 'amount_total': amount_untaxed + amount_tax,
                    # 'amount_total': amount_untaxed,
                }
            )

    def get_partidas_count(self):
        for r in self:
            r.partidas_count = self.env["partidas.partidas"].search_count(
                [("subcapitulo_id", "=", self.id)]
            )

    ###############
    # Actividades #
    ###############
    def get_acts_count(self):
        for r in self:
            count = self.env["mail.activity"].search_count(
                [("res_id", "=", self.id), ("res_model", "=", "sub.capitulo")]
            )
            r.activ_count = count if count else 0

    def met_activi_subcapitulo(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Actividades",
            "res_model": "mail.activity",
            "view_mode": "kanban,tree,form",
            "domain": [("res_id", "=", self.id), ("res_model", "=", "sub.capitulo")],
        }

    def action_view_partidas(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Partidas",
            "res_model": "partidas.partidas",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.partidas_ids.ids)],
            "context": dict(
                self._context,
                default_subcapitulo_id=self.id,
                default_project_id=self.project_id.id,
                default_fase_principal_id=self.fase_principal_id.id,
                default_capitulo_id=self.capitulo_id.id,
            ),
        }

    def wizard_cambio_precio(self):
        return {
            "name": "Cambiar Precio Masivo desde Subcapitulo",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "cambio.precio",
            "context": {
                "default_is_vacio": True,
                "default_subcapitulo_id": self.id,
                "default_info": "LOS PRECIOS SERAN CAMBIADOS A PARTIR DE </br>"
                + "<strong>"
                + str(self.capitulo_id.project_id.name)
                + "/"
                + str(self.fase_principal_id.name)
                + "/"
                + str(self.capitulo_id.name)
                + "/"
                + str(self.name)
                + " :</strong>",
            },
            "type": "ir.actions.act_window",
            "target": "new",
        }

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        # if self.partidas_ids:
        #     default['partidas_ids'] = self.partidas_ids.copy().ids // esto no borrar me queda de ejemplo para la eternidad

        record = super(Subcapitulo, self).copy(default)
        for partida in self.partidas_ids:
            record.partidas_ids |= partida.copy()

        return record

    def _compute_total_sub(self):
        for record in self:
            suma = 0.0
            for part in record.partidas_ids:
                if part.estado_partida == "aprobada":
                    suma += part.total
            record.update(
                {
                    # 'amount_untaxed': amount_untaxed,
                    "total": suma,
                    # 'amount_total': amount_untaxed + amount_tax,
                    # 'amount_total': amount_untaxed,
                }
            )

        #####################################
        ## Onchange para Agregar Las Fases ##
        #####################################
        @api.onchange("project_id")
        def _onchange_domain_project(self):
            fase = {}
            fase["domain"] = {
                "fase_principal_id": [("project_id", "=", self.project_id.id)]
            }
            return fase

        @api.onchange("fase_principal_id")
        def _onchange_domain_fase(self):
            cap = {}
            cap["domain"] = {
                "capitulo_id": [("fase_principal_id", "=", self.fase_principal_id.id)]
            }
            return cap

        # @api.onchange('capitulo_id')
        # def _onchange_domain_capitulo(self):
        #     sub = {}
        #     sub['domain'] = {'subcapitulo_id': [('capitulo_id', '=', self.capitulo_id.id)]}
        #     return sub
        ################################################################################################

    @api.model
    def create(self, values):
        project = self.env["project.project"].search(
            [("id", "=", values["project_id"])]
        )
        if project.stage_id.is_prevision:
            values.update(
                {
                    "estado": "aprobada",
                }
            )
        else:
            values.update(
                {
                    "estado": "pendiente",
                }
            )
        # Add code here
        return super(Subcapitulo, self).create(values)
