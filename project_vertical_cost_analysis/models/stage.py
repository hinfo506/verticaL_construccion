from odoo import fields, models, api
from odoo.exceptions import ValidationError


class VerticalStage(models.Model):
    _inherit = 'vertical.stage'

    cost_analysis_id = fields.Many2one(comodel_name='vertical.cost.analysis', string='Análisis de Coste', required=False)

    def add_cost_analysis(self):
        return {
            'name': 'Agregar Análisis de Coste',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.cost.analysis',
            # 'context': {
            #     'default_active_ids': act_ids,
            # },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }