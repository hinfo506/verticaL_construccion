from odoo import fields, models, api

class TypeStage(models.Model):
    _name = 'vertical.stage.type'

    name = fields.Char()
    sequence = fields.Integer(string='Sequence', required=False)
    is_end = fields.Boolean(string='Es final', required=False)
    is_additional = fields.Boolean(string='Adicionales', required=False)
