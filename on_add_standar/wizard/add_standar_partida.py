from odoo import fields, models, api


class AddStandar(models.TransientModel):
    _name = 'add.standar'

    standar_id = fields.Many2one(comodel_name='standard.request', string='Standar', required=False)
    cant_partidas = fields.Integer(string='Cantidad Partidas', required=False)
    # line_ids = fields.One2many('standard.request.line', 'request_id')
    line_ids = fields.Many2many(comodel_name='standard.request.line', string='Line_ids')
