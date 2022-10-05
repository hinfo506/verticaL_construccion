# -*- coding: utf-8 -*-

from odoo import models, fields


class Proyecto(models.Model):
    _inherit = 'project.project'

    directorios_id = fields.One2many(comodel_name='dms.directory', inverse_name='project_id', string='Directorios',
                                     required=False)

    directory_count = fields.Integer(string='Directorios', compute='get_directory_count')

    def get_directory_count(self):
        for r in self:
            count = self.env['dms.directory'].search_count([('project_id', '=', self.id)])
            r.directory_count = count if count else 0

    def met_directorios(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Directorios',
            'res_model': 'dms.directory',
            'view_mode': 'kanban,tree,form',
            'domain': [('id', 'in', self.directorios_id.ids)],
            'context': dict(self._context, default_project_id=self.id),
        }
