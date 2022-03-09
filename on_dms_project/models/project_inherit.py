# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Proyecto(models.Model):
    _inherit = 'project.project'

    directorios_id = fields.One2many(comodel_name='dms.directory', inverse_name='project_id', string='Directorios',
                                   required=False)

    directory_count = fields.Integer(string='Contador de Capitulos', compute='get_count_capitulos')

    def get_count_capitulos(self):
        count = self.env['dms.directory'].search_count([('project_id', '=', self.id)])
        self.directory_count = count


    def met_directorios(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Directorios',
            'res_model': 'dms.directory',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.directorios_id.ids)],
            'context': dict(self._context, default_project_id=self.id),
        }
