from odoo import fields, models, api
from odoo.exceptions import ValidationError

class VerticalStage(models.Model):
    _inherit = 'vertical.stage'

    def add_standars(self):
        act_ids = self.env.context.get('active_ids')
        return {
            'name': 'Add Standard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.standard',
            'context': {
                'default_active_ids': act_ids,
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
