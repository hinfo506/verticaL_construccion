# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Proyecto(models.Model):
    _inherit = 'project.project'

    directorios_id = fields.One2many(comodel_name='dms.directory', inverse_name='project_id', string='Directorios',
                                   required=False)
    def met_directorios(self):
        # raise ValidationError("estoy dentrop")
        # self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Directorios',
            'res_model': 'dms.directory',
            'view_mode': 'tree,form',
            # 'domain': [('id', 'in', self.directorios_id.ids)],
            # 'context': dict(self._context, default_project_id=self.id),
            # 'context': dict(self._context, default_vehiculo=self.vehicle_id.id, default_inscription_id=self.id,
            #                 default_partner_id=self.purchaser_id.id)
        }
