from odoo import fields, models, api


class Directorios(models.Model):
    _inherit = 'dms.directory'

    project_id = fields.Many2one('project.project', string='Proyecto')
    # capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo')
    # sub_capitulo_id = fields.Many2one('sub.capitulo', string='Sub Capitulo')
    # partida_id = fields.Many2one('partidas.partidas', string='Partida')
    # fase_principal_id = fields.Many2one('fase.principal', string='Partida')


