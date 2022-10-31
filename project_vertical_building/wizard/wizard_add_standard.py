from odoo import fields, models, api
from odoo.exceptions import ValidationError


class AddStandar(models.TransientModel):
    _name = "wizard.standard"

    standard_id = fields.Many2one(comodel_name="standard", string="Standard", required=False)
    active_ids = fields.Many2many(comodel_name="vertical.stage", string="Actividades")
    list_ids = fields.Many2many(comodel_name="standard.line", string="Lineas")
    active_id = fields.Many2one(comodel_name="vertical.stage", string="Actividad", required=False)
    is_one = fields.Boolean(string="Is_one", required=False)

    @api.onchange("standard_id")
    def _onchange_standards(self):
        for record in self:
            if record.standard_id:
                data = [("standard_id", "=", record.standard_id.id)]
                line = self.env["standard.line"].search(data)
                record.list_ids = line

    def action_insertar(self):
        if self.is_one:
            for line in self.list_ids:
                self.env["vertical.item"].create(
                    {
                        "vertical_stage_id": self.active_id.id,
                        "project_id": self.active_id.project_id.id,
                        "type_item": 'standard',
                        # "standar_id": self.id,
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
                    }
                )
        else:
            for active in self.active_ids:
                for line in self.list_ids:
                    record = self.env["vertical.item"].create(
                        {
                            "vertical_stage_id": active.id,
                            "project_id": active.project_id.id,
                            "type_item": 'standard',
                            # "standar_id": self.id,
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
                        }
                    )
