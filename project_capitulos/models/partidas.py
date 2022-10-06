from odoo import fields, models, api, _


class Partidas(models.Model):
    _name = "partidas.partidas"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    ###### DATOS PRINCIPALES  ########
    number = fields.Char(
        string="Number",
        required=True,
        copy=False,
        readonly="True",
        default=lambda self: self.env["ir.sequence"].next_by_code("secuencia.partidas"),
    )
    numero_partida = fields.Char(string="Número Partida", required=False)
    name = fields.Char(string="Partida", required=True)
    descripcion = fields.Text("Descripción de la Partida")
    cantidad = fields.Integer("Cantidad")
    fecha_inicio = fields.Date("Fecha Inicio")
    fecha_finalizacion = fields.Date("Acaba el")

    total = fields.Float("Importe Total", compute="_compute_total_parti")
    total_prevision = fields.Float("Importe Total Previsto")

    # Campo de Prueba para poder aprobar o no aprobar
    estado_partida = fields.Selection(
        string="Estado_partida",
        selection=[
            ("borrador", "Borrador"),
            ("aprobada", "Aprobada en Prevision"),
            ("aprobadaproceso", "Aprobada en Proceso"),
            ("pendiente", "Pdte Validar"),
            ("noaprobada", "No aprobada"),
        ],
        required=False,
        default="borrador",
    )

    condicion = fields.Selection(
        string="Condición",
        selection=[
            ("presupuestario", "Presupuestario"),
            ("sobrecoste", "Sobre Coste"),
            ("adicionales", "Adicionales"),
        ],
        required=False,
    )

    ###### FASES DEL PROYECTO ########
    project_id = fields.Many2one("project.project", string="Proyecto", required=True)
    fase_principal_id = fields.Many2one(
        comodel_name="fase.principal", string="Fase Principal", required=True
    )
    capitulo_id = fields.Many2one("capitulo.capitulo", string="Capitulo", required=True)
    subcapitulo_id = fields.Many2one(
        "sub.capitulo", string="Subcapitulo", ondelete="cascade", required=True
    )
    volumetria_ids = fields.One2many(
        comodel_name="volumetria.volumetria",
        inverse_name="partida_id",
        string=_("Volumetría"),
    )

    ###### CONTADORES  ########
    activi_count_parti = fields.Integer(
        string="Contador Actividades", compute="get_acti_count"
    )

    @api.onchange("number", "capitulo_id", "subcapitulo_id")
    def _onchange_join_number(self):
        self.numero_partida = (
            str(self.subcapitulo_id.numero_subcapitulo) + "." + str(self.number)
        )

    material_total = fields.Float(
        string="Total Coste Materiales", compute="_amount_all", readonly="True"
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
                material_total += line.suma_impuesto_item_y_cost_price
            order.update(
                {
                    # 'amount_untaxed': amount_untaxed,
                    "material_total": material_total,
                    # 'amount_total': amount_untaxed + amount_tax,
                    # 'amount_total': amount_untaxed,
                }
            )

    #############################
    ## Prueba despues quitamos ##
    #############################
    item_capitulo_ids = fields.One2many(
        comodel_name="item.capitulo",
        inverse_name="partidas_id",
        string="Materiales",
    )
    ##############################################

    item_capitulo_materiales_ids = fields.One2many(
        comodel_name="item.capitulo",
        inverse_name="partidas_id",
        string="Materiales",
        domain=[("job_type", "=", "material")],
    )
    item_mano_obra_ids = fields.One2many(
        comodel_name="item.capitulo",
        inverse_name="partidas_id",
        string="Mano de Obra",
        domain=[("job_type", "=", "labour")],
    )
    item_capitulo_gastos_generales = fields.One2many(
        comodel_name="item.capitulo",
        inverse_name="partidas_id",
        string="Gastos Generales",
        copy=False,
        domain=[("job_type", "=", "overhead")],
    )

    item_capitulo_maquinaria = fields.One2many(
        comodel_name="item.capitulo",
        inverse_name="partidas_id",
        string="Maquinaria",
        domain=[("job_type", "=", "machinery")],
    )

    item_count = fields.Integer(string="Contador Item", compute="get_item_count")

    def get_item_count(self):
        for r in self:
            r.item_count = self.env["item.capitulo"].search_count(
                [("partidas_id", "=", self.id)]
            )

    def action_view_item(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Items",
            "res_model": "item.capitulo",
            "view_mode": "tree,form",
            # 'domain': [('partidas_id', '=',  self.id)],
            "domain": [("id", "in", self.item_capitulo_ids.ids)],
            "views": [
                (
                    self.env.ref("project_capitulos.itemsubcapitulo_view_tree").id,
                    "tree",
                ),
                (
                    self.env.ref("project_capitulos.itemsubcapitulo_view_form").id,
                    "form",
                ),
            ],
            "context": dict(
                self._context,
                default_partidas_id=self.id,
                default_faseprincipal_id=self.fase_principal_id.id,
            ),
        }

    def wizard_cambio_precio(self):
        return {
            "name": "Cambiar Precio Masivo desde Partidas",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "cambio.precio",
            "context": {
                "default_is_vacio": True,
                "default_partida_id": self.id,
                "default_info": "LOS PRECIOS SERAN CAMBIADOS A PARTIR DE </br>"
                + "/<strong>"
                + str(self.subcapitulo_id.capitulo_id.project_id.name)
                + "/"
                + str(self.fase_principal_id.name)
                + "/"
                + str(self.subcapitulo_id.capitulo_id.name)
                + "/"
                + str(self.subcapitulo_id.name)
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

        record = super(Partidas, self).copy(default)
        for material in self.item_capitulo_materiales_ids:
            record.item_capitulo_materiales_ids |= material.copy()

        for mano_obra in self.item_mano_obra_ids:
            record.item_mano_obra_ids |= mano_obra.copy()

        for gasto_general in self.item_capitulo_gastos_generales:
            record.item_capitulo_gastos_generales |= gasto_general.copy()

        for maquinaria in self.item_capitulo_maquinaria:
            record.item_capitulo_maquinaria |= maquinaria.copy()

        for volumetria_id in self.volumetria_ids:
            record.volumetria_ids |= volumetria_id.copy()

        return record

    volumetria_count = fields.Integer(
        string="Contador Volumetria", compute="get_volumetria_count"
    )

    def get_volumetria_count(self):
        for r in self:
            r.volumetria_count = self.env["volumetria.volumetria"].search_count(
                [("partida_id", "=", self.id)]
            )

    def action_view_volumetria(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Volumetria",
            "res_model": "volumetria.volumetria",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.volumetria_ids.ids)],
            "context": dict(self._context, default_partida_id=self.id),
        }

    def get_acti_count(self):
        for r in self:
            count = self.env["mail.activity"].search_count(
                [("res_id", "=", self.id), ("res_model", "=", "partidas.partidas")]
            )
            r.activi_count_parti = count if count else 0

    def met_activi_partidas(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Actividades",
            "res_model": "mail.activity",
            "view_mode": "kanban,tree,form",
            "domain": [
                ("res_id", "=", self.id),
                ("res_model", "=", "partidas.partidas"),
            ],
        }

    def _compute_total_parti(self):
        for order in self:
            suma = 0.0
            for item in order.item_capitulo_ids:
                suma += item.suma_impuesto_item_y_cost_price
            order.update(
                {
                    # 'amount_untaxed': amount_untaxed,
                    "total": suma,
                    # 'amount_total': amount_untaxed + amount_tax,
                    # 'amount_total': amount_untaxed,
                }
            )
