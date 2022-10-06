from odoo import fields, models


class Etapa(models.Model):
    _name = 'stage.stage'

    name = fields.Char(string='Nombre')
