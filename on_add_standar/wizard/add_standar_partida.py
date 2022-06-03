from odoo import fields, models, api


class AddStandar(models.TransientModel):
    _name = 'add.standar'

    standard_id = fields.Many2one(comodel_name='standard', string='Standar', required=False)
    cant_partidas = fields.Integer(string='Cantidad Partidas', required=False)
    # line_ids = fields.One2many('standard.request.line', 'request_id')
    line_ids = fields.Many2many(comodel_name='standard.line', string='Line_ids')

    # Fases
    subcapitulo_id = fields.Many2one(comodel_name='sub.capitulo', string='Subcapitulo', required=False)

    @api.onchange('standard_id')
    def _onchange_standard(self):
        for record in self:
            if record.standard_id:
                data = [('standard_id', '=', record.standard_id.id)]
                line = self.env['standard.line'].search(data)
                record.line_ids = line

    def action_guardar(self):
        partida = self.env['partidas.partidas'].create({
            'name': self.standard_id.name,
            'subcapitulo_id': self.subcapitulo_id.id,
            'capitulo_id': self.subcapitulo_id.capitulo_id.id,
            'fase_principal_id': self.subcapitulo_id.fase_principal_id.id,
            'project_id': self.subcapitulo_id.project_id.id,
        })

        for line in self.line_ids:
            items = self.env['item.capitulo'].create({
                'cost_price': 1,
                'partidas_id': partida.id,
                'subcapitulo_id': self.subcapitulo_id.id,
                'capitulo_id': self.subcapitulo_id.capitulo_id.id,
                'faseprincipal_id': self.subcapitulo_id.fase_principal_id.id,
                'project_id': self.subcapitulo_id.project_id.id,
                'product_id': line.product_id.id,
                'product_qty': line.qty,
                'descripcion': line.descripcion,
            })
