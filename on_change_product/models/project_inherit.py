from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = 'project.project'

    def write(self, values):

        if values.get('stage_id'):
            stage = self.sudo().env['project.project.stage'].search([('id', '=', values.get('stage_id'))])
            if stage.is_prevision == False and self.total_prevision == 0:
                values['total_prevision'] = self.total

                record = super(Project, self).write(values)

                # Fase Principal
                fase_ids = self.env['fase.principal'].search([('project_id', '=', self.id)])
                for fase in fase_ids:
                    # raise ValidationError(fase.total)
                    fase.sudo().write({
                        'total_prevision': fase.total,
                    })

                # Capitulo
                capitulo_ids = self.env['capitulo.capitulo'].search([('project_id', '=', self.id)])
                for cap in capitulo_ids:
                    # raise ValidationError(fase.total)
                    cap.sudo().write({
                        'total_prevision': cap.total,
                    })

                return record

            else:
                return super(Project, self).write(values)
        else:
            return super(Project, self).write(values)

