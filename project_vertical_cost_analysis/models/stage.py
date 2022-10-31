import logging
from odoo import fields, models, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class VerticalStage(models.Model):
    _inherit = 'vertical.stage'


    cost_analysis_id = fields.Many2one(comodel_name='vertical.cost.analysis', string='Análisis de Coste', required=False)
    itemcost_count = fields.Integer(string='Itemcost_count', required=False, compute='get_item_cost_count')

    def get_item_cost_count(self):
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


        for line in record.cost_analysis_id.cost_analysis_line_ids:
            record.env["vertical.item"].create(
                {
                    "vertical_stage_id": record.id,
                    "project_id": record.project_id.id,
                    "type_item": 'cost_analysis',
                    "cost_analysis_id": record.cost_analysis_id.id,
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
            for l in record.cost_analysis_id.standard_id.line_ids:
                record.env["vertical.item"].create(
                    {
                        "vertical_stage_id": record.id,
                        "project_id": record.project_id.id,
                        "type_item": 'standard',
                        "cost_analysis_id": record.cost_analysis_id.id,
                        # "standar_id": self.cost_analysis_id.standard_id.id,
                        "job_type": l.job_type,
                        "product_id": l.product_id.id,
                        "descripcion": l.descripcion,
                        "uom_id": l.uom_id.id,
                        "product_qty": l.product_qty,
                        "cost_price": l.cost_price,
                        "subtotal_item_capitulo": l.subtotal_item_capitulo,
                        "tipo_descuento": l.tipo_descuento,
                        "cantidad_descuento": l.cantidad_descuento,
                        "subtotal_descuento": l.subtotal_descuento,
                        "impuesto_porciento": l.impuesto_porciento,
                        "total_impuesto_item": l.total_impuesto_item,
                        "beneficio_estimado": l.beneficio_estimado,
                        "importe_venta": l.importe_venta,
                        "suma_impuesto_item_y_cost_price": l.suma_impuesto_item_y_cost_price,
                    }
                )
        return record

    def write(self, values):
        record = super(VerticalStage, self).write(values)
        if values.get("cost_analysis_id"):
            if self.cost_analysis_id:
                for line in self.cost_analysis_id.cost_analysis_line_ids:
                    self.env["vertical.item"].create(
                        {
                            "vertical_stage_id": self.id,
                            "project_id": self.project_id.id,
                            "type_item": 'cost_analysis',
                            "cost_analysis_id": self.cost_analysis_id.id,
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
                    for l in self.cost_analysis_id.standard_id.line_ids:
                        self.env["vertical.item"].create(
                            {
                                "vertical_stage_id": self.id,
                                "project_id": self.project_id.id,
                                "type_item": 'standard',
                                "cost_analysis_id": self.cost_analysis_id.id,
                                # "standar_id": self.cost_analysis_id.standard_id.id,
                                "job_type": l.job_type,
                                "product_id": l.product_id.id,
                                "descripcion": l.descripcion,
                                "uom_id": l.uom_id.id,
                                "product_qty": l.product_qty,
                                "cost_price": l.cost_price,
                                "subtotal_item_capitulo": l.subtotal_item_capitulo,
                                "tipo_descuento": l.tipo_descuento,
                                "cantidad_descuento": l.cantidad_descuento,
                                "subtotal_descuento": l.subtotal_descuento,
                                "impuesto_porciento": l.impuesto_porciento,
                                "total_impuesto_item": l.total_impuesto_item,
                                "beneficio_estimado": l.beneficio_estimado,
                                "importe_venta": l.importe_venta,
                                "suma_impuesto_item_y_cost_price": l.suma_impuesto_item_y_cost_price,
                            }
                        )
                    return record
                else:
                    return record
        else:
            return record

    def on_delete_ac(self):
        for record in self:
            value_unlink = self.env['vertical.item'].search([('cost_analysis_id', '=', record.cost_analysis_id.id),('vertical_stage_id', '=', record.id),('project_id', '=', record.project_id.id)]).unlink()
            record.cost_analysis_id = []

    is_ac_true = fields.Boolean(string='Is_ac_true', required=False, compute='method_is_ac_true')

    def method_is_ac_true(self):
        for record in self:
            if record.cost_analysis_id:
                record.is_ac_true = True
            else:
                record.is_ac_true = False

