from odoo import fields, models, api


class Directorios(models.Model):
    _inherit = 'dms.directory'

    project_id = fields.Many2one('project.project', string='Proyecto')

