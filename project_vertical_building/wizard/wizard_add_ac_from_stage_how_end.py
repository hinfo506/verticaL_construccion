from odoo import fields, models, api
from odoo.exceptions import ValidationError


class AddAcHowStageEnd(models.TransientModel):
    _name = 'wizard.add.ac'

    # name = fields.Char()
    cant = fields.Integer(string='Cantidad', required=False)
    code = fields.Char(string='Código', required=False)
    cost_analysis_id = fields.Many2one(
        comodel_name='vertical.cost.analysis',
        string='Análisis de Coste',
        required=False)
    fecha_inicio = fields.Date("Fecha Inicio")
    fecha_finalizacion = fields.Date("Acaba el")

    active_ids = fields.Many2many(comodel_name="vertical.stage", string="Ids activos")

    def action_insertar(self):
        stage_end = self.env['vertical.stage.type'].search([('is_end', '=', True)])
        for active in self.active_ids:
            stage = self.env["vertical.stage"].create(
                {
                    "project_id": active.project_id.id,
                    "type_stage_id": stage_end.id,
                    "name_complete": self.cost_analysis_id.name,
                    "name": self.cost_analysis_id.name,
                    "cost_analysis_id": self.cost_analysis_id.id,
                    "parent_id": active.id,
                    # "numero_fase": self.,
                    "cantidad": self.cant,
                    "fecha_inicio": self.fecha_inicio,
                    "fecha_finalizacion": self.fecha_finalizacion,
                }
            )
            for line in self.cost_analysis_id.cost_analysis_line_ids:
                item_ac = self.env["vertical.item"].create(
                    {
                        "cost_analysis_id": self.cost_analysis_id.id,
                        "project_id": active.project_id.id,
                        "cost_stage_id": stage.id,
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
            for line in self.cost_analysis_id.standard_id.line_ids:
                item_stand = self.env["vertical.item"].create(
                    {
                        "standard_id": self.cost_analysis_id.standard_id.id,
                        "project_id": active.project_id.id,
                        "standard_stage_id": stage.id,
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
