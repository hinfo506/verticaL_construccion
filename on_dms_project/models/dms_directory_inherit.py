from odoo import fields, models, api


class Directorios(models.Model):
    _inherit = 'dms.directory'

    project_id = fields.Many2one('project.project', string='Proyecto')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulos')
    sub_capitulo_id = fields.Many2one('sub.capitulo', string='Sub Capitulos')

