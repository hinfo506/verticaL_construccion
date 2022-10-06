from odoo import fields, models, api


class VerticalStage(models.Model):
    _inherit = 'vertical.stage'

    bills_ids = fields.One2many(comodel_name='vertical.bills', inverse_name='stage_id', string='Bills_ids',
                                required=False)
    bills_count = fields.Integer(string='Contador Gastos', compute='get_bills_count')

    @api.depends('bills_ids')
    def get_bills_count(self):
        for r in self:
            # r.bills_count = self.env['vertical.bills'].search_count([('stage_id', '=', self.id)])
            r.bills_count = len(r.bills_ids)

    def action_view_bills(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Gastos',
            'res_model': 'vertical.bills',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.bills_ids.ids)],
            # 'views': [(self.env.ref('project_vertical_building.item_view_tree').id, 'tree'),
            #           (self.env.ref('project_vertical_building.item_view_form').id, 'form')],
            'context': dict(self._context, default_stage_id=self.id),
        }
