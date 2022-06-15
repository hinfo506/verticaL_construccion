from odoo import fields, models, api


class FasePrincipal(models.Model):
    _inherit = 'fase.principal'

    def on_change_product(self):
        return {
            'name': 'Cambiar Producto',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'change.product',
            'context': {
                'default_faseprincipal_id': self.id,
                'default_info': "LOS PRODUCTOS SERAN CAMBIADOS A PARTIR DE </br><strong>" + str(
                    self.project_id.name) + "/" + str(self.name) + " :</strong>",
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
