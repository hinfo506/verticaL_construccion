from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = 'project.project'

    def on_change_product(self):
        return {
            'name': 'Cambiar Producto',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'change.product',
            'context': {
                'default_project_id': self.id,
                'default_info': "LOS PRECIOS SERAN CAMBIADOS A PARTIR DE </br><strong>"+str(self.name)+" :</strong>",
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
