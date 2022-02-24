from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError,RedirectWarning

class Subcapitulo(models.Model):
    _name = 'sub.capitulo'

    name = fields.Char(string='Sub-Capitulo', required=True)
    descripcion = fields.Text('Descripción del Sub-Capitulo')
    total = fields.Float('Importe Total')
    fecha_finalizacion = fields.Date('Fecha Finalización')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo')

    number = fields.Char(string='Number', required=True, copy=False, readonly='True',
                       default=lambda self: self.env['ir.sequence'].next_by_code('secuencia.subcapitulo'))
    
    numero = fields.Char(string='Numero', required=False)

    @api.onchange('number')
    def _onchange_FIELD_NAME(self):


        # raise ValidationError(self.capitulo_id.numero_capitulo)
        self.numero = str(self.capitulo_id.numero_capitulo) + "." + str(self.number)

    material_total = fields.Float(string='Total Coste Materiales', readonly='True')
    labor_total = fields.Float(string='Total Coste Horas', readonly='True')
    overhead_total = fields.Float(string='Total Costes Generales', readonly='True')
    jobcost_total = fields.Float(string='Total Coste', readonly='True')

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
        string='Gatos Generales',
        copy=False,
        domain=[('job_type', '=', 'overhead')],
    )


class ItemCapitulo(models.Model):
    _name = 'item.capitulo'

    name = fields.Char(string='Sub-Capitulo', required=True)
    total = fields.Float('Importe Total')
    fecha_finalizacion = fields.Date('Fecha Finalización')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo')
    subcapitulo_id = fields.Many2one('sub.capitulo', string='Capitulo')

    descripcion = fields.Text(u'Descripción')

    # Agregados del modulo original
    date = fields.Date(string='Fecha',required=True,copy=False,)
    reference = fields.Char(string='Referencia', copy=False,)
    product_qty = fields.Float(string='Cantidad Planificada',copy=False,)
    uom_id = fields.Many2one('uom.uom', string='Uom',)
    cost_price = fields.Float(string='Cost / Unit',copy=False,)
    product_id = fields.Many2one(comodel_name='product.product', string='Producto')

    # actual_quantity = fields.Float(string='Actual Purchased Quantity',compute='_compute_actual_quantity',)
    actual_quantity = fields.Float(string='Cantidad Comprada Actual',)

    # total_cost = fields.Float(string='Cost Price Sub Total',compute='_compute_total_cost',store=True,)
    total_cost = fields.Float(string='Precio Costo Sub Total',store=True,)

    hours = fields.Char(string='Horas', required=False)
    actual_timesheet = fields.Char(string='Parte de Horas Actual', required=False)
    basis = fields.Char(string='Base', required=False)

    job_type = fields.Selection(
        selection=[('material', 'Materiales'),
                   ('labour', 'Mano de Obra'),
                   ('overhead', 'Gastos Generales')],
        string="Tipo de Costo",
        required=False,)