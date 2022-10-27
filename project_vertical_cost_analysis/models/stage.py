import logging
from odoo import fields, models, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class VerticalStage(models.Model):
    _inherit = 'vertical.stage'


    cost_analysis_id = fields.Many2one(comodel_name='vertical.cost.analysis',string='Cost_analysis_id', required=False)
    itemcost_count = fields.Integer(string='Itemcost_count', required=False, compute='get_item_cost_count')

    def get_item_cost_count(self):
        for r in self:
            r.itemcost_count = self.env['vertical.item'].search_count([("id", "in", self.item_ids.ids), ("type_item", "=", 'cost_analysis')])
            # r.item_count = len(r.item_ids)

    def action_view_item_cost(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Items",
            "res_model": "vertical.item",
            "view_mode": "tree,form",
            # 'domain': [('partidas_id', '=',  self.id)],
            "domain": [("id", "in", self.item_ids.ids), ("type_item", "=", 'cost_analysis')],
            # "views": [
            #     (self.env.ref("project_vertical_building.item_view_tree").id, "tree"),
            #     (self.env.ref("project_vertical_building.item_view_form").id, "form"),
            # ],
            # "context": dict(
            #     self._context,
            #     default_vertical_stage_id=self.id,
            #     default_project_id=self.project_id.id,
            # ),
        }

    # def action_insertar(self):
    #     for line in self.list_ids:
    #         # raise ValidationError(self.active_id)
    #         self.env["vertical.item"].create(
    #             {
    #                 "vertical_stage_id": self.active_id.id,
    #                 "project_id": self.active_id.project_id.id,
    #                 "type_item": 'standard',
    #                 # "standar_id": self.id,
    #                 "job_type": line.job_type,
    #                 "product_id": line.product_id.id,
    #                 "descripcion": line.descripcion,
    #                 "uom_id": line.uom_id.id,
    #                 "product_qty": line.product_qty,
    #                 "cost_price": line.cost_price,
    #                 "subtotal_item_capitulo": line.subtotal_item_capitulo,
    #                 "tipo_descuento": line.tipo_descuento,
    #                 "cantidad_descuento": line.cantidad_descuento,
    #                 "subtotal_descuento": line.subtotal_descuento,
    #                 "impuesto_porciento": line.impuesto_porciento,
    #                 "total_impuesto_item": line.total_impuesto_item,
    #                 "beneficio_estimado": line.beneficio_estimado,
    #                 "importe_venta": line.importe_venta,
    #                 "suma_impuesto_item_y_cost_price": line.suma_impuesto_item_y_cost_price,
    #             }
    #         )

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
            # raise ValidationError(self.active_id)
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
        return record

    def write(self, values):
        record = super(VerticalStage, self).write(values)
        _logger.info("Error al crear usuario: ")
        # if values.get("cost_analysis_id") == 0:
        #     raise ValidationError('has editado el analisis de coste')
        if values.get("cost_analysis_id"):

            if self.cost_analysis_id:
                old_value = self._origin.cost_analysis_id

                # raise ValidationError(old_value)
                value_unlink = self.env['vertical.item'].search([('cost_analysis_id', '=', old_value.id)]).unlink()
                for line in self.cost_analysis_id.cost_analysis_line_ids:
                    # raise ValidationError(self.active_id)
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
                    return record
                else:
                    return record

        else:
            return record

    # def create_analisis_coste(self):
