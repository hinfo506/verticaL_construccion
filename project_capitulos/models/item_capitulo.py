from odoo import fields, models, api


class ItemCapitulo(models.Model):
    _name = 'item.capitulo'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    total = fields.Float('Importe Total')
    fecha_finalizacion = fields.Date('Fecha Finalización')
    descripcion = fields.Text('Descripción')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo',ondelete='cascade')
    subcapitulo_id = fields.Many2one('sub.capitulo', string='Subcapitulo',ondelete='cascade')
    partidas_id = fields.Many2one('partidas.partidas', string='Partidas',ondelete='cascade')
    project_id = fields.Many2one('project.project', string='Proyecto')

    longitud = fields.Float('Longitud', default=1)
    ancho = fields.Float('Ancho', default=1)
    alto = fields.Float('Alto', default=1)
    impuesto_item = fields.Float('Imp. %', default=18)
    
    date = fields.Date(string='Fecha', default=lambda self: fields.Date.today())
    product_id = fields.Many2one(comodel_name='product.product', string='Producto')
    reference = fields.Char(string='Referencia', copy=False, )
    product_qty = fields.Float(string='Cantidad Planificada', copy=False, digits=(12,2))
    uom_id = fields.Many2one('uom.uom', string='Unid. de Medida', )
    cost_price = fields.Float(string='Precio Coste', copy=False, )
    actual_quantity = fields.Float(string='Cantidad Comprada Actual', )
    hours = fields.Char(string='Horas', required=False)
    actual_timesheet = fields.Char(string='Parte de Horas Actual', required=False)
    basis = fields.Char(string='Base', required=False)

    # Campos Sumatorios
    item_volumetria_ids = fields.One2many(comodel_name='item.volumetria', inverse_name='itemcapitulo_id',string='Item Volumetria', required=False)
    itemvolumetria_count = fields.Integer(string='Itemvolumetria_count', required=False, compute='get_itemvolu_count')

    # Campos Con Seleccion
    job_type = fields.Selection(
        selection=[('material', 'Materiales'),
                   ('labour', 'Mano de Obra'),
                   ('overhead', 'Gastos Generales'),
                   ('machinery', 'Maquinaria')],
        string="Tipo de Costo",
        required=False, )
    
    color_item_id = fields.Selection(
        selection=[('red', 'Rojo'),
                   ('blue', 'Azul'),
                   ('green', 'Verde'),
                   ('grey', 'Gris'),
                   ('brown', 'Marrón'),
                   ('purple', 'Púrpura')],

        string="Color de la Linea",
        required=False,)


    # Campos de variables calculadas
    subtotal_item_capitulo = fields.Float(string='Subtotal', store=False, compute='_compute_subtotal_item_capitulo')
    total_impuesto_item = fields.Float(string='ITBIS', store=False, compute='_compute_total_impuesto_item')
    total_item_capitulo = fields.Float(string='Total', store=False, compute='_compute_total_item_capitulo')
    suma_impuesto_item_y_cost_price = fields.Float(string='P.U. + ITBIS', store=False, compute='_compute_suma_impuesto_item_y_cost_price')


    #############################################################################

    # Importe Subtotal item Capitulo - Importe sin contar con los impuestos
    @api.depends('product_qty', 'cost_price', 'longitud', 'ancho', 'alto')
    def _compute_subtotal_item_capitulo(self):
        for rec in self:
            if rec.job_type == 'material':
                rec.subtotal_item_capitulo = rec.product_qty * rec.cost_price
            elif rec.job_type == 'labour':
                rec.subtotal_item_capitulo = rec.product_qty * rec.cost_price
            elif rec.job_type == 'machinery':
                rec.subtotal_item_capitulo = rec.product_qty * 3  # AQUI TIENE QUE IR, EN VEZ DE EL 3 EL TOTAL DE MATERIAL + LABOUR Y QUE PRODUCT_QTY SEA UN %
            else:
                rec.subtotal_item_capitulo = 0

    # Importe Total Impuesto Item - Importe de los impuestos a partir del campo impuesto_item
    @api.depends('cost_price', 'impuesto_item')
    def _compute_total_impuesto_item(self):
        for rec in self:
                rec.total_impuesto_item = rec.cost_price * rec.impuesto_item / 100

    # Suma Impuesto item + Precio de Coste - Suma del precio unitario del producto + el impuesto
    @api.depends('product_qty', 'cost_price','total_impuesto_item')
    def _compute_suma_impuesto_item_y_cost_price(self):
        for rec in self:
                rec.suma_impuesto_item_y_cost_price = rec.cost_price + rec.total_impuesto_item
    
    # Importe Total Item Capitulo - Total Item Capitulo incluido impuestos
    @api.depends('product_qty', 'suma_impuesto_item_y_cost_price')
    def _compute_total_item_capitulo(self):
        for rec in self:
                rec.total_item_capitulo = rec.suma_impuesto_item_y_cost_price * rec.product_qty

    @api.onchange('product_id')
    def _onchan_product_id(self):
        for rec in self:
            rec.descripcion = rec.product_id.name
            rec.product_qty = 1.0
            rec.uom_id = rec.product_id.uom_id.id
            rec.cost_price = rec.product_id.standard_price  # lst_price

    
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
        }

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        record = super(ItemCapitulo, self).copy(default)
        for volumetria in self.item_volumetria_ids:
            record.item_volumetria_ids |= volumetria.copy()

        return record