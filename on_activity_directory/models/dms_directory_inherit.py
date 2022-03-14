# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Directorios(models.Model):
    _inherit = 'dms.directory'

    # activities_id = fields.Many2one('mail.activity', string='Actividades')
    activities_id = fields.One2many(comodel_name='mail.activity', inverse_name='directory_id', string='Actividades', required=False)

    activities_count = fields.Integer(string='Directorios', compute='get_activities_count')

    def get_activities_count(self):
        for r in self:
            count = self.env['mail.activity'].search_count([('directory_id', '=', self.id)])
            r.activities_count = count if count else 0

    def met_actividades(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Actividades',
            'res_model': 'mail.activity',
            'view_mode': 'kanban,tree,form',
            'domain': [('id', 'in', self.activities_id.ids)],
            'context': dict(self._context, default_directory_id=self.id),
        }
