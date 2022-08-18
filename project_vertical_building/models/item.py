from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError,RedirectWarning


class VerticalItem(models.Model):
    _name = 'vertical.item'
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

    total_prevision = fields.Float('Importe Total Previsto')


    date = fields.Date(string='Fecha', default=lambda self: fields.Date.today())
    fecha_finalizacion = fields.Date('Fecha Finalización')

    condicion = fields.Selection(string='Condición', selection=[
        ('presupuestario', 'Presupuestario'),
        ('sobrecoste', 'Sobre Coste'),
        ('adicionales', 'Adicionales'), ], required=False, )

    ###### FASES DEL PROYECTO ######## 
    project_id = fields.Many2one('project.project', string='Proyecto', ondelete='cascade')
    vertical_stage_id = fields.Many2one(comodel_name='vertical.stage',string='Fase', required=False)

    ###### CAMPOS DESECHADOS ######## 
    longitud = fields.Float('Longitud', default=1)
    ancho = fields.Float('Ancho', default=1)
    alto = fields.Float('Alto', default=1)

    item_volumetry_ids = fields.One2many(comodel_name='vertical.item.volumetry', inverse_name='item_id',string='Item Volumetria', required=False)

    # Campos Sumatorios
    item_volumetry_count = fields.Integer(string='item_volumetry_count', required=False, compute='get_item_volumetry_count')

    # Campos Con Seleccion
    job_type = fields.Selection(
        selection=[('material', 'Materiales'),
                   ('labour', 'Mano de Obra'),
                   ('overhead', 'Gastos Generales'),
                   ('machinery', 'Maquinaria')],
        string="Tipo de Costo",
        required=True, )
    
    color_item = fields.Selection(
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
    #############################################################################

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            rec.descripcion = rec.product_id.name
            rec.product_qty = 1.0
            rec.uom_id = rec.product_id.uom_id.id
            rec.cost_price = rec.product_id.standard_price  # lst_price

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
    
    def get_item_volumetry_count(self):
        for r in self:
            r.item_volumetry_count = self.env['vertical.item.volumetry'].search_count([('item_id', '=', self.id)])

    def met_itemvolumetria(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Volumetria',
            'res_model': 'vertical.item.volumetry',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.item_volumetry_ids.ids)],
            'context': dict(self._context, default_item_id=self.id),
        }

    estado_item = fields.Selection(
        string='Estado_partida',
        selection=[('borrador', 'Borrador'),
                   ('aprobada', 'Aprobada en Prevision'),
                   ('aprobadaproceso', 'Aprobada en Proceso'),
                   ('pendiente', 'Pdte Validar'),
                   ('noaprobada', 'No aprobada'), ],
        required=False, default='borrador')

    @api.model
    def create(self, vals):
        project = self.sudo().env['project.project'].search([('id', '=', vals['project_id'])])
        # raise ValidationError(project.stage_id.name)

        # if vals['add_standar']:
        if project.stage_id.is_prevision:
            # raise ValidationError('esta en prevision')
            vals.update({
                'estado_item': 'aprobada',
            })
        else:
            vals.update({
                'estado_item': 'pendiente',
            })

        return super(VerticalItem, self).create(vals)
