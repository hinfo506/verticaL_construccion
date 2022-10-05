# -*- coding: utf-8 -*-

from odoo import fields, models


class Directorios(models.Model):
    _inherit = 'dms.directory'

    activities_count = fields.Integer(string='Directorios', compute='get_activities_count')

    def get_activities_count(self):
        for r in self:
            count = self.env['mail.activity'].search_count(
                [('res_id', '=', self.id), ('res_model', '=', 'dms.directory')])
            r.activities_count = count if count else 0

    def met_actividades(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Actividades',
            'res_model': 'mail.activity',
            'view_mode': 'kanban,tree,form',
            'domain': [('res_id', '=', self.id), ('res_model', '=', 'dms.directory')],
            # 'context': dict(self._context, default_directory_id=self.id),
        }
