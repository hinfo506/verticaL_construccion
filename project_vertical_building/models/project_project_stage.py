from odoo import fields, models, api

class ProjectStage(models.Model):
    _inherit = 'project.project.stage'

    is_prevision = fields.Boolean(string='Es Prevision', required=False)
    adicionales = fields.Selection(string='Adicionales', selection=[('si', 'SI'), ('no', 'NO'), ], required=False, )

