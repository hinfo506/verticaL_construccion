from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class ProyectosInherit(models.Model):
    _inherit = 'project.project'

    capitulos_id = fields.One2many(comodel_name='capitulo.capitulo', inverse_name='project_id', string='Capitulos_id', required=False)

    def met_capitulos(self):
        # raise ValidationError("estoy dentrop")
        # self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Capitulos',
            'res_model': 'capitulo.capitulo',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.project_id.ids)],
            # 'context': dict(self._context, default_vehiculo=self.vehicle_id.id, default_inscription_id=self.id,
            #                 default_partner_id=self.purchaser_id.id)
        }