# -*- coding: utf-8 -*-

from odoo import models, fields, api

class VerticalCostAnalysis(models.Model):
    _name = 'vertical.cost.analysis'

    name = fields.Char('Nombre')
    standard_id = fields.Many2one(comodel_name='standard', string='Standard')
    stage_ids = fields.One2many(comodel_name='vertical.stage', inverse_name='cost_analysis_id', string='Stage_id', required=False)
    cost_analysis_line_ids = fields.One2many(comodel_name='cost.analysis.line', inverse_name='cost_analysis_id', string='Cost_analysis_line_ids', required=False)
    cost_standard = fields.Float(string='', required=False, related='standard_id.total_cost')
    # cost_cost_analysis = fields.Float(string='Total Coste', required=False)
    cost_cost_analysis = fields.Float(string='Total Coste', required=False, compute='_calc_cost_total')

    def _calc_cost_total(self):
        # pass
        for record in self:
            sumatoria = 0
            if record.cost_standard or record.cost_analysis_line_ids:
                sumatoria = record.cost_standard + sum(c.suma_impuesto_item_y_cost_price for c in record.cost_analysis_line_ids)
                # record.cost_cost_analysis = record.cost_standard + sum(record.cost_analysis_line_ids.mapped("suma_impuesto_item_y_cost_price"))
                # sum(c.suma_impuesto_item_y_cost_price for c in record.cost_analysis_line_ids)
            record.cost_cost_analysis = sumatoria