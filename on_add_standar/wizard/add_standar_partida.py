from odoo import fields, models, api


class AddStandar(models.TransientModel):
    _name = 'add.standar'

    standard_id = fields.Many2one(comodel_name='standard', string='Standard', required=True)
    cant_partidas = fields.Integer(string='Cantidad Partida', required=False)
    info = fields.Html(string="Info", required=False)
    line_ids = fields.Many2many(comodel_name='standard.line', string='Line_ids')

    # Fases
    subcapitulo_id = fields.Many2one(comodel_name='sub.capitulo', string='Subcapitulo', required=False)

    number = fields.Char(string='Number', required=True, copy=False, readonly='True',
                         default=lambda self: self.env['ir.sequence'].next_by_code('secuencia.partidas'))

    @api.onchange('standard_id')
    def _onchange_standard(self):
        for record in self:
            if record.standard_id:
                data = [('standard_id', '=', record.standard_id.id)]
                line = self.env['standard.line'].search(data)
                record.line_ids = line

    def action_guardar(self):
        # 'depend_edad1': False if not (kw.get('depend_edad1')) else kw.get('depend_edad1'),

        partida = self.env['partidas.partidas'].create({
            'name': self.standard_id.name,
            'cantidad': self.cant_partidas,
            'numero_partida': str(self.subcapitulo_id.numero_subcapitulo) + '.' + str(self.number),
            'estado_partida': 'pendiente' if not self.subcapitulo_id.project_id.stage_id.is_prevision else 'aprobada',
            'subcapitulo_id': self.subcapitulo_id.id,
            'capitulo_id': self.subcapitulo_id.capitulo_id.id,
            'add_standar': False,
            'fase_principal_id': self.subcapitulo_id.fase_principal_id.id,
            'project_id': self.subcapitulo_id.project_id.id,
        })

        for line in self.line_ids:
            items = self.env['item.capitulo'].create({
                'partidas_id': partida.id,
                'subcapitulo_id': self.subcapitulo_id.id,
                'capitulo_id': self.subcapitulo_id.capitulo_id.id,
                'faseprincipal_id': self.subcapitulo_id.fase_principal_id.id,
                'project_id': self.subcapitulo_id.project_id.id,
                'cost_price': line.cost_price,
                'product_id': line.product_id.id,
                'uom_id': line.uom_id.id,
                'product_qty': line.qty,
                'descripcion': line.descripcion,
                'job_type': line.job_type,
                'subtotal_item_capitulo': line.subtotal_item_capitulo,
                'tipo_descuento': line.tipo_descuento,
                'cantidad_descuento': line.cantidad_descuento,
                'subtotal_descuento': line.subtotal_descuento,
                'beneficio_estimado': line.beneficio_estimado,
                'importe_venta': line.importe_venta,
                'impuesto_porciento': line.impuesto_porciento,
                'total_impuesto_item': line.total_impuesto_item,
                'suma_impuesto_item_y_cost_price': line.suma_impuesto_item_y_cost_price,
            })

        # standard_requests = self.env['standard.request'].create({
        #     'subcapitulo_id': self.subcapitulo_id.id,
        #     'capitulo_id': self.subcapitulo_id.capitulo_id.id,
        #     'fase_principal_id': self.subcapitulo_id.fase_principal_id.id,
        #     'project_id': self.subcapitulo_id.project_id.id,
        #     'partida_id': partida.id,
        #     'state': 'pendiente',
        #     'standard_id': self.standard_id.id,
        #     'cant_partidas': self.cant_partidas,
        # })

        return {
            'name': 'Partidas',
            'res_model': 'partidas.partidas',
            'view_mode': 'tree',
            'domain': [('subcapitulo_id', '=', self.subcapitulo_id.id)],
            'views': [(self.env.ref('project_capitulos.partidas_view_tree').id, 'tree'),(self.env.ref('project_capitulos.partidas_view_form').id, 'form')],
            # 'target': 'new',
            'context': dict(self._context, default_subcapitulo_id=self.subcapitulo_id.id),
            'type': 'ir.actions.act_window',
        }