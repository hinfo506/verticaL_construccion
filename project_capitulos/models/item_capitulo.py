from odoo import fields, models, api


class ItemCapitulo(models.Model):
    _name = 'item.capitulo'

    # name = fields.Char(string='Sub-Capitulo', required=True)
    total = fields.Float('Importe Total')
    fecha_finalizacion = fields.Date('Fecha Finalización')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo')
    subcapitulo_id = fields.Many2one('sub.capitulo', string='Subcapitulo')
    longitud = fields.Float('Longitud', default=1)
    ancho = fields.Float('Ancho', default=1)
    alto = fields.Float('Alto', default=1)

    #############################################################################

    # Cantidad (Uds * LONGITUD * ANCHURA * ALTURA)

    # @api.depends('product_qty', 'longitud', 'ancho', 'alto')
    # def _compute_cantidad_costo(self):
    # for rec in self:
    # rec.cantidad_cost = rec.product_qty * rec.longitud * rec.ancho * rec.alto

    # Precio Total Subcapitulo Materiales
    @api.depends('product_qty', 'cost_price', 'longitud', 'ancho', 'alto')
    def _compute_total_costo(self):
        for rec in self:
            if rec.job_type == 'material':
                # rec.cantidad_cost = rec.product_qty * rec.longitud * rec.ancho * rec.alto // INCLUIDO LONGITUD, ANCHO Y ALTO: VOLUMETRIA
                # rec.total_cost = rec.cantidad_cost * rec.cost_price
                rec.total_cost = rec.product_qty * rec.cost_price
            elif rec.job_type == 'labour':
                rec.total_cost = rec.product_qty * rec.cost_price
            elif rec.job_type == 'machinery':
                rec.total_cost = rec.product_qty * 3  # AQUI TIENE QUE IR, EN VEZ DE EL 3 EL TOTAL DE MATERIAL + LABOUR Y QUE PRODUCT_QTY SEA UN %
            else:
                rec.total_cost = 0

    # declaracion de variables calculadas

    total_cost = fields.Float(string='Total Subcapitulo', store=False, compute='_compute_total_costo')
    descripcion = fields.Text('Descripción')
    # cantidad_cost = fields.Float(string='Cantidad Por LO-AN-AL', store=False, compute='_compute_cantidad_costo')
    # total_cost = fields.Float(string='Cost Price Sub Total',compute='_compute_total_costo',store=True,)

    # Agregados del modulo original
    date = fields.Date(string='Fecha', default=lambda self: fields.Date.today())
    product_id = fields.Many2one(comodel_name='product.product', string='Producto')
    reference = fields.Char(string='Referencia', copy=False, )
    product_qty = fields.Float(string='Cantidad Planificada', copy=False, )
    uom_id = fields.Many2one('uom.uom', string='Unid. de Medida', )
    cost_price = fields.Float(string='Precio Coste', copy=False, )
    longitud = fields.Float(string='Longitud', required=False)
    ancho = fields.Float(string='Ancho', required=False)
    altura = fields.Float(string='Altura', required=False)

    # actual_quantity = fields.Float(string='Actual Purchased Quantity',compute='_compute_actual_quantity',)
    actual_quantity = fields.Float(string='Cantidad Comprada Actual', )

    hours = fields.Char(string='Horas', required=False)
    actual_timesheet = fields.Char(string='Parte de Horas Actual', required=False)
    basis = fields.Char(string='Base', required=False)

    job_type = fields.Selection(
        selection=[('material', 'Materiales'),
                   ('labour', 'Mano de Obra'),
                   ('overhead', 'Gastos Generales'),
                   ('machinery', 'Gastos Generales')],
        string="Tipo de Costo",
        required=False, )

    @api.onchange('product_id')
    def _onchan_product_id(self):
        for rec in self:
            rec.descripcion = rec.product_id.name
            rec.product_qty = 1.0
            rec.uom_id = rec.product_id.uom_id.id
            rec.cost_price = rec.product_id.standard_price  # lst_price

    item_volumetria_ids = fields.One2many(comodel_name='item.volumetria', inverse_name='itemcapitulo_id',string='Item Volumetria', required=False)
    itemvolumetria_count = fields.Integer(string='Itemvolumetria_count', required=False, compute='get_itemvolu_count')

    def get_itemvolu_count(self):
        for r in self:
            r.itemvolumetria_count = self.env['item.volumetria'].search_count([('itemcapitulo_id', '=', self.id)])

    def met_itemvolumetria(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Volumetria',
            'res_model': 'item.volumetria',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.item_volumetria_ids.ids)],
            'context': dict(self._context, default_itemcapitulo_id=self.id),
            # 'context': dict(self._context, default_vehiculo=self.vehicle_id.id, default_inscription_id=self.id,
            #                 default_partner_id=self.purchaser_id.id)
        }