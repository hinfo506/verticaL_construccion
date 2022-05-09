from odoo import fields, models, api


class CambioPrecioMasivo(models.TransientModel):
    _name = 'cambio.precio'

    name = fields.Char()
