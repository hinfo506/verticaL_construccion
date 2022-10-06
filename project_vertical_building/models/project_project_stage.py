from odoo import fields, models


class ProjectStage(models.Model):
    _inherit = 'project.project.stage'

    is_prevision = fields.Boolean(string='Es Prevision', required=False)
