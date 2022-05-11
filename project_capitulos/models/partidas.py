from odoo import fields, models, api


class Partidas(models.Model):
    _name = 'partidas.partidas'

    subcapitulo_id = fields.Many2one(comodel_name='sub.capitulo', string='Subcapitulo id', required=False)
    name = fields.Char(string='Partida', required=True)
    descripcion = fields.Text('Descripción de la Partida')
    cantidad = fields.Integer('Cantidad')
    total = fields.Float('Importe Total')
    fecha_inicio = fields.Date('Fecha Inicio')
    fecha_finalizacion = fields.Date('Acaba el')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo')
    subcapitulo_id = fields.Many2one('sub.capitulo', string='Subcapitulo')
    number = fields.Char(string='Number', required=True, copy=False, readonly='True',
                         default=lambda self: self.env['ir.sequence'].next_by_code('secuencia.partidas'))
    numero_partida = fields.Char(string='Número Partida', required=False)

    @api.onchange('number', 'capitulo_id','subcapitulo_id')
    def _onchange_join_number(self):
        self.numero_partida = str(self.subcapitulo_id.numero_subcapitulo) + "." + str(self.number)


    material_total = fields.Float(string='Total Coste Materiales', compute='_amount_all' ,readonly='True')
    labor_total = fields.Float(string='Total Coste Mano de Obra', readonly='True')
    machinerycost_total = fields.Float(string='Total Coste Maquinaria', readonly='True')
    overhead_total = fields.Float(string='Total Costes Generales', readonly='True')
    jobcost_total = fields.Float(string='Total Coste', readonly='True')

    # Calculos
    @api.depends('item_capitulo_materiales_ids')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = material_total = 0.0
            for line in order.item_capitulo_materiales_ids:
                # amount_untaxed += 1
                # amount_untaxed += line.price_subtotal
                material_total += line.total_item_capitulo
            order.update({
                # 'amount_untaxed': amount_untaxed,
                'material_total': material_total,
                # 'amount_total': amount_untaxed + amount_tax,
                # 'amount_total': amount_untaxed,
            })



    item_capitulo_materiales_ids = fields.One2many(
        comodel_name='item.capitulo',
        inverse_name='partidas_id',
        string='Materiales',
        domain=[('job_type', '=', 'material')],
    )
    item_mano_obra_ids = fields.One2many(
        comodel_name='item.capitulo',
        inverse_name='partidas_id',
        string='Mano de Obra',
        domain=[('job_type', '=', 'labour')],
    )
    item_capitulo_gastos_generales = fields.One2many(
        comodel_name='item.capitulo',
        inverse_name='partidas_id',
        string='Gastos Generales',
        copy=False,
        domain=[('job_type', '=', 'overhead')],
    )

    item_capitulo_maquinaria = fields.One2many(
        comodel_name='item.capitulo',
        inverse_name='partidas_id',
        string='Maquinaria',
        domain=[('job_type', '=', 'machinery')],
    )

    item_count = fields.Integer(string='Contador Item', compute='get_item_count')

    def get_item_count(self):
        for r in self:
            r.item_count = self.env['item.capitulo'].search_count([('partidas_id', '=',  self.id)])

    def action_view_item(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Items',
            'res_model': 'item.capitulo',
            'view_mode': 'tree,form',
            'domain': [('partidas_id', '=',  self.id)],
            'views': [(self.env.ref('project_capitulos.itemsubcapitulo_view_tree').id, 'tree'), (self.env.ref('project_capitulos.itemsubcapitulo_view_form').id, 'form')],
            'context': dict(self._context, default_partidas_id=self.id),
        }

    def wizard_cambio_precio(self):
        # raise ValidationError(self.id)
        return {
            'name': 'Cambiar Precio Masivo desde Partidas',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cambio.precio',
            'context': {
                'default_partida_id': self.id,
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }