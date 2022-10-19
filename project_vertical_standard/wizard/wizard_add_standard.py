from odoo import fields, models, api
from odoo.exceptions import ValidationError


class AddStandar(models.TransientModel):
    _name = "wizard.standard"

    standard_id = fields.Many2one(
        comodel_name="standard", string="Standard", required=False
    )
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
                # raise ValidationError(self.active_id)
                self.env["vertical.item"].create(
                    {
                        "vertical_stage_id": self.active_id.id,
                        "project_id": self.active_id.project_id.id,
                        # "standar_id": self.id,
                        "job_type": line.job_type,
                        "product_id": line.product_id.id,
                        "descripcion": line.descripcion,
                        "uom_id": line.uom_id.id,
                        "product_qty": line.product_qty,
                        "cost_price": line.cost_price,
                        "subtotal_item_capitulo": line.subtotal_item_capitulo,#ver si necesito enviarlo
                        "tipo_descuento": line.tipo_descuento,
                        "cantidad_descuento": line.cantidad_descuento,
                        "subtotal_descuento": line.subtotal_descuento,#ver si necesito enviarlo
                        "impuesto_porciento": line.impuesto_porciento,
                        "total_impuesto_item": line.total_impuesto_item,#ver si necesito enviarlo
                        "beneficio_estimado": line.beneficio_estimado,
                        "importe_venta": line.importe_venta,#ver si necesito enviarlo
                        "suma_impuesto_item_y_cost_price": line.suma_impuesto_item_y_cost_price,#ver si necesito enviarlo
                    }
                )
        else:
            for active in self.active_ids:
                for line in self.list_ids:
                    self.env["vertical.item"].create(
                        {
                            "vertical_stage_id": self.active_id.id,
                            "project_id": self.active_id.project_id.id,
                            # "standar_id": self.id,
                            "job_type": line.job_type,
                            "product_id": line.product_id.id,
                            "descripcion": line.descripcion,
                            "uom_id": line.uom_id.id,
                            "product_qty": line.product_qty,
                            "cost_price": line.cost_price,
                            "subtotal_item_capitulo": line.subtotal_item_capitulo,#ver si necesito enviarlo
                            "tipo_descuento": line.tipo_descuento,
                            "cantidad_descuento": line.cantidad_descuento,
                            "subtotal_descuento": line.subtotal_descuento,#ver si necesito enviarlo
                            "impuesto_porciento": line.impuesto_porciento,
                            "total_impuesto_item": line.total_impuesto_item,#ver si necesito enviarlo
                            "beneficio_estimado": line.beneficio_estimado,
                            "importe_venta": line.importe_venta,#ver si necesito enviarlo
                            "suma_impuesto_item_y_cost_price": line.suma_impuesto_item_y_cost_price,#ver si necesito enviarlo
                        }
                    )
