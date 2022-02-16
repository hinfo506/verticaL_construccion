from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class ProyectosInherit(models.Model):
    _inherit = 'project.project'

    capitulos_id = fields.One2many(comodel_name='capitulo.capitulo', inverse_name='project_id', string='Capitulos_id', required=False)
    capitulos_count = fields.Integer(string='Contador de Capitulos', compute='get_count_capitulos')

    def get_count_capitulos(self):
        count = self.env['capitulo.capitulo'].search_count([('project_id', '=', self.id)])
        self.capitulos_count = count


    def met_capitulos(self):
        # raise ValidationError("estoy dentrop")
        # self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Capitulos',
            'res_model': 'capitulo.capitulo',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.capitulos_id.ids)],
            'context': dict(self._context, default_project_id=self.id),
            # 'context': dict(self._context, default_vehiculo=self.vehicle_id.id, default_inscription_id=self.id,
            #                 default_partner_id=self.purchaser_id.id)
        }