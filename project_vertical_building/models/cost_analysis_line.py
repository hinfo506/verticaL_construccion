from odoo import fields, models

class CostAnalysisLine(models.Model):
    _name = 'cost.analysis.line'
    _inherit = "item.item"

    cost_analysis_id = fields.Many2one('vertical.cost.analysis', string='Estandar')
