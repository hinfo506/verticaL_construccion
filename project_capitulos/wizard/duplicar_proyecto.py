from odoo import fields, models, api


class DuplicarProyecto(models.TransientModel):
    _name = 'duplicar.proyecto'

    name = fields.Char()
