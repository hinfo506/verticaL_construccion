from odoo import fields, models, api

class TypeStage(models.Model):
    _name = 'vertical.stage.type'

    name = fields.Char()
    sequence = fields.Integer(string='Sequence', required=False)
    is_end = fields.Boolean(string='Es final', required=False)
    adicionales = fields.Selection(string='Adicionales', selection=[('si', 'Si'), ('no', 'No'), ], required=False, )
