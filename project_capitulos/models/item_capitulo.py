from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError,RedirectWarning


class ItemCapitulo(models.Model):
    _name = 'item.capitulo'
    _rec_name = 'product_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ##### DATOS PRINCIPALES  ########
    product_id = fields.Many2one(comodel_name='product.product', string='Producto')
    reference = fields.Char(string='Referencia', copy=False, )
    descripcion = fields.Text('Descripción')
    product_qty = fields.Float(string='Cantidad Planificada', copy=False, digits=(12,2))
    uom_id = fields.Many2one('uom.uom', string='Unid. de Medida', )
    cost_price = fields.Float(string='Precio Coste', copy=False, )
    actual_quantity = fields.Float(string='Cantidad Comprada Actual', )
    hours = fields.Char(string='Horas', required=False)
    actual_timesheet = fields.Char(string='Parte de Horas Actual', required=False)
    basis = fields.Char(string='Base', required=False)
    # impuesto_item = fields.Float('Imp. %', default=18)

    # total = fields.Float('Importe Total')
    total_prevision = fields.Float('Importe Total Previsto')


    date = fields.Date(string='Fecha', default=lambda self: fields.Date.today())
    fecha_finalizacion = fields.Date('Fecha Finalización')

    condicion = fields.Selection(string='Condición', selection=[
        ('presupuestario', 'Presupuestario'),
        ('sobrecoste', 'Sobre Coste'),
        ('adicionales', 'Adicionales'), ], required=False, )

    ###### FASES DEL PROYECTO ######## 
    project_id = fields.Many2one('project.project', string='Proyecto',ondelete='cascade')
    faseprincipal_id = fields.Many2one('fase.principal', string='Fase Principal', ondelete='cascade')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo',ondelete='cascade')
    subcapitulo_id = fields.Many2one('sub.capitulo', string='Subcapitulo',ondelete='cascade')
    partidas_id = fields.Many2one('partidas.partidas', string='Partidas',ondelete='cascade')

    ###### CAMPOS DESECHADOS ######## 
    longitud = fields.Float('Longitud', default=1)
    ancho = fields.Float('Ancho', default=1)
    alto = fields.Float('Alto', default=1)

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
        required=True, )
    
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
    # total_impuesto_item = fields.Float(string='ITBIS', store=False, compute='_compute_total_impuesto_item')
    # total_item_capitulo = fields.Float(string='Total', store=False, compute='_compute_total_item_capitulo')
    # suma_impuesto_item_y_cost_price = fields.Float(string='P.U. + ITBIS', store=False, compute='_compute_suma_impuesto_item_y_cost_price')
    #############################################################################
    
    # Calculos de descuentos por impuestos creados por Raul
    tipo_descuento = fields.Selection(string='Tipo descuento Proveedor', selection=[('cantidad', 'cantidad'), ('porciento', 'porciento'), ('sindescuento', 'sindescuento'), ], required=False, default='sindescuento' )
    cantidad_descuento = fields.Float(string='Cantidad Descuento', required=False)
    subtotal_descuento = fields.Float(string='Subtotal Con descuento', required=False, compute='_compute_subtotal_descuento', store=False)
    beneficio_estimado = fields.Float(string='Beneficio Estimado en %', required=False)
    importe_venta = fields.Float(string='Importe Venta (PVP)', required=False, compute='_compute_subtotal_descuento', store=False)
    impuesto_porciento = fields.Float(string='Impuesto en % (ITBIS)', required=False)
    total_impuesto_item = fields.Float(string='Importe ITBIS', required=False, compute='_compute_subtotal_descuento', store=False)
    suma_impuesto_item_y_cost_price = fields.Float(string='Total (P.U. + ITBIS)', required=False, compute='_compute_subtotal_descuento', store=False)

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

    # Importe Subtotal item Capitulo - Importe con los impuestos
    @api.depends('tipo_descuento','product_qty', 'cost_price', 'subtotal_item_capitulo', 'cantidad_descuento','beneficio_estimado','impuesto_porciento')
    def _compute_subtotal_descuento(self):
        for record in self:
            if record.tipo_descuento == 'cantidad':
                record.subtotal_descuento = record.subtotal_item_capitulo - record.cantidad_descuento
            elif record.tipo_descuento == 'porciento':
                record.subtotal_descuento = record.subtotal_item_capitulo - ((record.subtotal_item_capitulo*record.cantidad_descuento)/100)
            else:
                record.subtotal_descuento = record.subtotal_item_capitulo

            record.importe_venta = ((record.subtotal_item_capitulo * record.beneficio_estimado) / 100) + record.subtotal_item_capitulo
            record.total_impuesto_item = record.subtotal_descuento * (record.impuesto_porciento / 100)
            record.suma_impuesto_item_y_cost_price = record.subtotal_descuento + record.total_impuesto_item

    # Importe Total Impuesto Item - Importe de los impuestos a partir del campo impuesto_item
    # @api.depends('cost_price', 'impuesto_item')
    # def _compute_total_impuesto_item(self):
    #     for rec in self:
    #             rec.total_impuesto_item = rec.cost_price * rec.impuesto_item / 100

    # Suma Impuesto item + Precio de Coste - Suma del precio unitario del producto + el impuesto
    # @api.depends('product_qty', 'cost_price','total_impuesto_item')
    # def _compute_suma_impuesto_item_y_cost_price(self):
    #     for rec in self:
    #             rec.suma_impuesto_item_y_cost_price = rec.cost_price + rec.total_impuesto_item
    
    # Importe Total Item Capitulo - Total Item Capitulo incluido impuestos
    # @api.depends('product_qty', 'suma_impuesto_item_y_cost_price')
    # def _compute_total_item_capitulo(self):
    #     for rec in self:
    #             rec.total_item_capitulo = rec.suma_impuesto_item_y_cost_price * rec.product_qty

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