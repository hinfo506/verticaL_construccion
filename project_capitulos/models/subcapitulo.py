from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError,RedirectWarning

class Subcapitulo(models.Model):
    _name = 'sub.capitulo'

    name = fields.Char(string='Subcapítulo', required=True)
    descripcion = fields.Text('Descripción del Subcapítulo')
    cantidad = fields.Integer('Cantidad')
    total = fields.Float('Importe Total')
    fecha_inicio = fields.Date('Fecha Inicio')
    fecha_finalizacion = fields.Date('Acaba el')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo')

    number = fields.Char(string='Number', required=True, copy=False, readonly='True',
                       default=lambda self: self.env['ir.sequence'].next_by_code('secuencia.subcapitulo'))
    
    numero = fields.Char(string='Numero', required=False)

    @api.onchange('number','capitulo_id')
    def _onchange_join_number(self):
        self.numero = str(self.capitulo_id.numero_capitulo) + "." + str(self.number)

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
                material_total += line.total_cost
            order.update({
                # 'amount_untaxed': amount_untaxed,
                'material_total': material_total,
                # 'amount_total': amount_untaxed + amount_tax,
                # 'amount_total': amount_untaxed,
            })



    item_capitulo_materiales_ids = fields.One2many(
        comodel_name='item.capitulo',
        inverse_name='subcapitulo_id',
        string='Materiales',
        domain=[('job_type', '=', 'material')],
    )
    item_mano_obra_ids = fields.One2many(
        comodel_name='item.capitulo',
        inverse_name='subcapitulo_id',
        string='Mano de Obra',
        domain=[('job_type', '=', 'labour')],
    )
    item_capitulo_gastos_generales = fields.One2many(
        comodel_name='item.capitulo',
        inverse_name='subcapitulo_id',
        string='Gastos Generales',
        copy=False,
        domain=[('job_type', '=', 'overhead')],
    )

    item_capitulo_maquinaria = fields.One2many(
        comodel_name='item.capitulo',
        inverse_name='subcapitulo_id',
        string='Maquinaria',
        domain=[('job_type', '=', 'machinery')],
    )

    ###############
    # Actividades #
    ###############
    activ_count = fields.Integer(string='Contador actividades', compute='get_acts_count')

    def get_acts_count(self):
        for r in self:
            count = self.env['mail.activity'].search_count([('res_id', '=', self.id),('res_model','=','sub.capitulo')])
            r.activ_count = count if count else 0

    def met_activi_subcapitulo(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Actividades',
            'res_model': 'mail.activity',
            'view_mode': 'kanban,tree,form',
            'domain': [('res_id', '=',  self.id),('res_model','=','sub.capitulo')],
            #'context': dict(self._context, default_directory_id=self.id),
        }


class ItemCapitulo(models.Model):
    _name = 'item.capitulo'
        
    # name = fields.Char(string='Sub-Capitulo', required=True)
    total = fields.Float('Importe Total')
    fecha_finalizacion = fields.Date('Fecha Finalización')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo')
    subcapitulo_id = fields.Many2one('sub.capitulo', string='Subcapitulo')
    longitud = fields.Float('Longitud', default = 1)
    ancho = fields.Float('Ancho', default = 1)
    alto = fields.Float('Alto', default = 1)

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
                rec.total_cost = rec.product_qty * 3 # AQUI TIENE QUE IR, EN VEZ DE EL 3 EL TOTAL DE MATERIAL + LABOUR Y QUE PRODUCT_QTY SEA UN %

   

    # declaracion de variables calculadas

    total_cost = fields.Float(string='Total Subcapitulo', store=False, compute='_compute_total_costo')  
    descripcion = fields.Text('Descripción')
    # cantidad_cost = fields.Float(string='Cantidad Por LO-AN-AL', store=False, compute='_compute_cantidad_costo')
    # total_cost = fields.Float(string='Cost Price Sub Total',compute='_compute_total_costo',store=True,)

    # Agregados del modulo original
    date = fields.Date(string='Fecha',default=lambda self: fields.Date.today())
    product_id = fields.Many2one(comodel_name='product.product', string='Producto')
    reference = fields.Char(string='Referencia', copy=False,)
    product_qty = fields.Float(string='Cantidad Planificada',copy=False,)
    uom_id = fields.Many2one('uom.uom', string='Unid. de Medida',)
    cost_price = fields.Float(string='Precio Coste',copy=False,)
    longitud = fields.Float(string='Longitud', required=False)
    ancho = fields.Float(string='Ancho', required=False)
    altura = fields.Float(string='Altura', required=False)
    

    # actual_quantity = fields.Float(string='Actual Purchased Quantity',compute='_compute_actual_quantity',)
    actual_quantity = fields.Float(string='Cantidad Comprada Actual',)

    hours = fields.Char(string='Horas', required=False)
    actual_timesheet = fields.Char(string='Parte de Horas Actual', required=False)
    basis = fields.Char(string='Base', required=False)

    job_type = fields.Selection(
        selection=[('material', 'Materiales'),
                   ('labour', 'Mano de Obra'),
                   ('overhead', 'Gastos Generales'),
                   ('machinery', 'Gastos Generales')],
        string="Tipo de Costo",
        required=False,)

    @api.onchange('product_id')
    def _onchan_product_id(self):
        for rec in self:
            rec.descripcion = rec.product_id.name
            rec.product_qty = 1.0
            rec.uom_id = rec.product_id.uom_id.id
            rec.cost_price = rec.product_id.standard_price  # lst_price