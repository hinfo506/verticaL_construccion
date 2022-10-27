from odoo import fields, models, api


class VerticalItem(models.Model):
    _inherit = 'vertical.item'

    cost_analysis_id = fields.Many2one(comodel_name='vertical.cost.analysis', string='cost_analysis_id', required=False)
