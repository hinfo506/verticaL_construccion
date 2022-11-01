from odoo import fields, models, api
from odoo.exceptions import ValidationError


class VerticalStage(models.Model):
    _name = "vertical.stage"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    ###### DATOS PRINCIPALES  ########
    numero_fase = fields.Char(string="Número Fase", required=False, track_visibility="always")
    name = fields.Char(string="Nombre Fase", required=True)
    name_complete = fields.Char(string="Nombre Completo", required=True)
    descripcion = fields.Text("Descripción de la Partida")
    cantidad = fields.Integer("Cantidad", default=1)
    fecha_inicio = fields.Date("Fecha Inicio")
    fecha_finalizacion = fields.Date("Acaba el")

    total = fields.Float("Precio Coste", compute="_compute_total_fase")

    # Campo  aprobar o no aprobar fase
    estado_fase = fields.Selection(string="Estado_partida",
                                   selection=[
                                       ("borrador", "Borrador"),
                                       ("aprobada", "Aprobada en Prevision"),
                                       ("aprobadaproceso", "Aprobada en Proceso"),
                                       ("pendiente", "Pdte Validar"),
                                       ("noaprobada", "No aprobada"), ], required=False, default="borrador",)

    item_ids = fields.One2many(
        comodel_name="vertical.item",
        inverse_name="vertical_stage_id",
        string="Items",
    )
    project_id = fields.Many2one(comodel_name="project.project", string="Proyecto", required=False)

    parent_id = fields.Many2one(comodel_name="vertical.stage", string="Depende de", required=False)
    child_ids = fields.One2many(
        comodel_name="vertical.stage",
        inverse_name="parent_id",
        string="Childs",
        required=False,
    )

    related_is_prevision = fields.Boolean("Es prevision", related="project_id.stage_id.is_prevision")

    # Calculos Generales
    material_total = fields.Float(string="Total Coste Materiales", compute="_compute_amount_all", readonly="True")
    labor_total = fields.Float(string="Total Coste Mano de Obra", readonly="True")
    machinerycost_total = fields.Float(string="Total Coste Maquinaria", readonly="True")
    overhead_total = fields.Float(string="Total Costes Generales", readonly="True")
    jobcost_total = fields.Float(string="Total Coste", readonly="True")

    type_stage_id = fields.Many2one(comodel_name="vertical.stage.type", string="Tipo de Fase", required=False)
    related_is_end = fields.Boolean("Is_End", related="type_stage_id.is_end")
    total2 = fields.Float("Precio Total", compute="_compute_total")

    item_count = fields.Integer(string="Contador Item", compute="_compute_item_count")
    childs_count = fields.Integer(string="Contador Childs", compute="_compute_childs_count")

    # Cost Analysis
    cost_analysis_id = fields.Many2one(comodel_name='vertical.cost.analysis', string='Análisis de Coste',
                                       required=False)
    itemcost_count = fields.Integer(string='Itemcost_count', required=False, compute='_compute_item_cost_count')

    # Standard
    itemstand_count = fields.Integer(string='Itemstand_count', required=False, compute='_compute_item_stand_count')

    def _compute_item_stand_count(self):
        for r in self:
            r.itemstand_count = self.env['vertical.item'].search_count(
                [("id", "in", self.item_ids.ids), ("type_item", "=", 'standard')])

    def action_view_item_standard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Items",
            "res_model": "vertical.item",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.item_ids.ids), ("type_item", "=", 'standard')],
        }

    def add_standars(self):
        act_ids = self.env.context.get('active_ids')
        active_ids = self.env['vertical.stage'].search([('id', '=', act_ids)])

        # Comprobar que las fases a las que se va a agregar el standar sean partidas
        for active in active_ids:
            if not active.type_stage_id.is_end:
                raise ValidationError('Debe seleccionar solo Fases de tipo Final')

        return {
            'name': 'Add Standard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.standard',
            'context': {
                'default_active_ids': act_ids,
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def add_standars_one_id(self):
        return {
            'name': 'Add Standard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.standard',
            'context': {
                'default_active_id': self.id,
                'default_is_one': True,
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
    ###########################################################

    # Cost Analysis
    def _compute_item_cost_count(self):
        for r in self:
            r.itemcost_count = self.env['vertical.item'].search_count([("id", "in", self.item_ids.ids), ("type_item", "=", 'cost_analysis')])

    def action_view_item_cost(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Items",
            "res_model": "vertical.item",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.item_ids.ids), ("type_item", "=", 'cost_analysis')],
        }

    @api.depends("item_ids")
    def _compute_amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            material_total = labour_total = 0.0
            machinery_total = overhead_total = 0.0
            for line in order.item_ids:
                # amount_untaxed += 1
                # amount_untaxed += line.price_subtotal
                if line.job_type == "material":
                    material_total += line.suma_impuesto_item_y_cost_price
                if line.job_type == "labour":
                    labour_total += line.suma_impuesto_item_y_cost_price
                if line.job_type == "machinery":
                    machinery_total += line.suma_impuesto_item_y_cost_price
                if line.job_type == "overhead":
                    overhead_total += line.suma_impuesto_item_y_cost_price
            order.update(
                {
                    # 'amount_untaxed': amount_untaxed,
                    "material_total": material_total,
                    "labor_total": labour_total,
                    "machinerycost_total": machinery_total,
                    "overhead_total": overhead_total,
                    # 'amount_total': amount_untaxed + amount_tax,
                    # 'amount_total': amount_untaxed,
                }
            )

    @api.depends("item_ids")
    def _compute_item_count(self):
        for r in self:
            r.item_count = len(r.item_ids)

    @api.depends("child_ids")
    def _compute_childs_count(self):
        for r in self:
            r.childs_count = len(r.child_ids)

    def action_view_item(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Items",
            "res_model": "vertical.item",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.item_ids.ids)],
            "views": [
                (self.env.ref("project_vertical_building.item_view_tree").id, "tree"),
                (self.env.ref("project_vertical_building.item_view_form").id, "form"),
            ],
            "context": dict(
                self._context,
                default_vertical_stage_id=self.id,
                default_project_id=self.project_id.id,
            ),
        }

    def action_view_childs(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Create Childs",
            "res_model": "vertical.stage",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.child_ids.ids)],
            "context": dict(self._context, default_parent_id=self.id),
        }

    def _compute_total_fase(self):

        for order in self:
            if order.type_stage_id.is_end:
                suma = 0.0
                for item in order.item_ids:
                    suma += item.suma_impuesto_item_y_cost_price
                order.update(
                    {
                        "total": suma,
                    }
                )
            else:
                suma = 0.0
                for fase in order.child_ids:
                    suma += fase.total
                order.update(
                    {
                        "total": suma,
                    }
                )

    def _compute_total(self):
        for record in self:
            if record.total != 0 and record.cantidad != 0:
                result = 0.0
                result = record.cantidad * record.total
                record.update(
                    {
                        "total2": result,
                    }
                )
            else:
                record.update(
                    {
                        "total2": 0,
                    }
                )

    def approve_fase(self):
        self.estado_fase = "aprobadaproceso"

    @api.model
    def create(self, vals):
        record = super(VerticalStage, self).create(vals)
        if (
                record.project_id
                and record.project_id.stage_id
                and record.project_id.stage_id.is_prevision
        ):
            state = (
                "aprobada" if record.project_id.stage_id.is_prevision else "pendiente"
            )
            record.write({"estado_fase": state})

        return record


    def on_delete_ac(self):
        for record in self:
            value_unlink = self.env['vertical.item'].search([
                ('cost_analysis_id', '=', record.cost_analysis_id.id),
                ('vertical_stage_id', '=', record.id),
                ('project_id', '=', record.project_id.id)]).unlink()
            # record.cost_analysis_id = []


    @api.onchange('cost_analysis_id')
    def onchange_project_id(self):
        if self.cost_analysis_id:
            self.item_ids = [(5, 0, {
                "vertical_stage_id": self.id,
                "project_id": self.project_id.id,
                # "type_item": 'cost_analysis',
                # "cost_analysis_id": self.cost_analysis_id.id,
                "standard_id": self.cost_analysis_id.standard_id.id,
                "job_type": line.job_type,
                "product_id": line.product_id.id,
                "descripcion": line.descripcion,
                "uom_id": line.uom_id.id,
                "product_qty": line.product_qty,
                "cost_price": line.cost_price,
                "subtotal_item_capitulo": line.subtotal_item_capitulo,
                "tipo_descuento": line.tipo_descuento,
                "cantidad_descuento": line.cantidad_descuento,
                "subtotal_descuento": line.subtotal_descuento,
                "impuesto_porciento": line.impuesto_porciento,
                "total_impuesto_item": line.total_impuesto_item,
                "beneficio_estimado": line.beneficio_estimado,
                "importe_venta": line.importe_venta,
                "suma_impuesto_item_y_cost_price": line.suma_impuesto_item_y_cost_price,
            }) for line in self.cost_analysis_id.cost_analysis_line_ids]
