from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class ProyectosInherit(models.Model):
    _inherit = 'project.project'

    def met_capitulos(self):
        raise ValidationError("estoy dentrop")
