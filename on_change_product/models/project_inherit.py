from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = 'project.project'

    # stage_id = fields.Many2one(
    #     comodel_name='project.project.stage',
    #     string='Stage_id',
    #     required=False)

    # @api.onchange('stage_id.name')
    # def _onchange_da(self):
    #     raise ValidationError('cambio el valor de stage_id')



    def write(self, values):

        if values.get('stage_id'):
            stage = self.sudo().env['project.project.stage'].search([('id', '=', values.get('stage_id'))])
            if stage.is_prevision == False and self.total_prevision == 0:
                values['total_prevision'] = self.total

        record = super(Project, self).write(values)

        fase_ids = self.env['fase.principal'].search([('project_id', '=', self.id)])
        # fase_ids = self.env['fase.principal'].browse([('project_id', '=', self.id)])
        # fase_ids.update({'total_prevision': fase.total})
        # raise ValidationError(self.fase_principal_ids)
        for fase in fase_ids:
            # raise ValidationError(fase.total)
            fase.sudo().write({
                'total_prevision': fase.total,
            })

        return record

    # items = self.env['item.capitulo'].browse(self.item_ids.ids)
    # items.write({'cost_price': self.nuevo_precio})
