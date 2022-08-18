from odoo import fields, models, api
from odoo.exceptions import ValidationError

class VerticalStage(models.Model):
    _inherit = 'vertical.stage'

    def add_standars(self):
        act_ids = self.env.context.get('active_ids')
        active_ids = self.env['vertical.stage'].search([('id', '=', act_ids)])

        # raise ValidationError(self.id)

        # Comprobar que las fases a las que se va a agregar el standar sean partidas
        for active in active_ids:
            if active.type_stage_id.is_end != True:
                raise ValidationError('Debe seleccionar solo partidas')
        
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

    def add_standars_one_id(self):
        # act_ids = self.env.context.get('active_ids')
        active_ids = self.env['vertical.stage'].search([('id', '=', self.id)])

        # raise ValidationError(active_ids)

        # Comprobar que las fases a las que se va a agregar el standar sean partidas
        # for active in active_ids:
        #     if active.type_stage_id.is_end != True:
        #         raise ValidationError('Debe seleccionar solo partidas')

        return {
            'name': 'Add Standard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.standard',
            'context': {
                'default_active_id': self.id,
                'default_is_one': True,
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
