from odoo import fields, models, api
from odoo.exceptions import ValidationError


class VerticalStage(models.Model):
    _inherit = 'vertical.stage'

    cost_analysis_id = fields.Many2one(comodel_name='vertical.cost.analysis', string='Análisis de Coste', required=False)

    # Depreciar este método
    @api.onchange('cost_analysis_id')
    def onchange_method(self):
        item_obj = self.env["vertical.item"]
        actual=self._origin.cost_analysis_id
        if self.cost_analysis_id:
            # raise ValidationError(self._origin.cost_analysis_id)
            delete_ids = self.env['vertical.item'].search([('cost_analysis_id', '=', actual.id)]).unlink()
            for line in self.cost_analysis_id.cost_analysis_line_ids:
                current_item = item_obj.create({
                            'vertical_stage_id': self.id,
                            'project_id': self.project_id.id,
                            'cost_price': line.cost_price,
                            'product_id': line.product_id.id,
                            'uom_id': line.uom_id.id,
                            'product_qty': line.qty,
                            'descripcion': line.descripcion,
                            'job_type': line.job_type,
                            'subtotal_item_capitulo': line.subtotal_item_capitulo,
                            'tipo_descuento': line.tipo_descuento,
                            'cantidad_descuento': line.cantidad_descuento,
                            'subtotal_descuento': line.subtotal_descuento,
                            'beneficio_estimado': line.beneficio_estimado,
                            'importe_venta': line.importe_venta,
                            'impuesto_porciento': line.impuesto_porciento,
                            'total_impuesto_item': line.total_impuesto_item,
                            'suma_impuesto_item_y_cost_price': line.suma_impuesto_item_y_cost_price,
                            'cost_analysis_id': self.cost_analysis_id.id,
                            # 'standar_id': self.id,
                        })
            # else:
            #     raise ValidationError('no tiene valor')
    
    # implementación de analisis de coste con campo computado
    # Este era el original
    # item_ids = fields.One2many(comodel_name='vertical.item', inverse_name='vertical_stage_id', string='Items', )
    # item_ids2 = fields.Many2many(
    #     'vertical.item',
    #     'item_stage_rel',
    #     'stage_id',
    #     'item_id',
    #     string='Items', compute="compute_item_ids", store=True)
    #
    # @api.depends('cost_analysis_id', 'cost_analysis_id.cost_analysis_line_ids')
    # def compute_item_ids(self):
    #     for stage in self:
    #         stage.item_ids2 = [(6, False, stage.cost_analysis_id.ids)]

    def action_view_standards(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Items Standars',
            'res_model': 'vertical.standard.item',
            'view_mode': 'tree,form',
            # 'domain': [('partidas_id', '=',  self.id)],
            'domain': [('id', 'in', self.item_ids.ids)],
            'views': [(self.env.ref('project_vertical_building.item_view_tree').id, 'tree'),
                      (self.env.ref('project_vertical_building.item_view_form').id, 'form')],
            'context': dict(self._context, default_vertical_stage_id=self.id,
                            default_project_id=self.project_id.id),
        }

    item_count = fields.Integer(string='Contador Item', compute='get_item_count_standars')

    @api.depends('item_ids')
    def get_item_count_standars(self):
        for r in self:
            # r.item_count = self.env['vertical.item'].search_count([('vertical_stage_id', '=', r.id)]) # Esta consulta es menos eficiente que simplemente contar los item_ids
            r.item_count = len(r.item_ids)
