from odoo import fields, models, api
from odoo.exceptions import ValidationError


class WizardCostAnalysis(models.TransientModel):
    _name = 'wizard.cost.analysis'

    name = fields.Char()

    cost_analysis_id = fields.Many2one(comodel_name='vertical.cost.analysis', string='Análisis de Coste', required=False)
    list_ids = fields.Many2many(comodel_name='standard.line', string='List_ids')

    @api.onchange('cost_analysis_id')
    def _onchange_cost_analysis_list(self):
        for record in self:
            if record.cost_analysis_id:
                data = [('standard_id', '=', record.cost_analysis_id.standard_id.id)]
                line = self.env['standard.line'].search(data)
                record.list_ids = line

    def action_insertar(self):
        raise ValidationError('abcdefuck')
