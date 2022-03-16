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
    subcapitulo_id = fields.Many2one('sub.capitulo', string='Capitulo')


    #############################################################################

    # Precio Total
    @api.depends('product_qty', 'cost_price')
    def _compute_total_costo(self):
        for rec in self:
            if rec.job_type == 'labour':
                rec.product_qty = 0.0
                rec.total_cost = rec.hours * rec.cost_price
            else:
                rec.hours = 0.0
                rec.total_cost = rec.product_qty * rec.cost_price

    # total_cost = fields.Float(string='Cost Price Sub Total',compute='_compute_total_costo',store=True,)
    total_cost = fields.Float(string='Precio Costo Sub Total', store=True, compute='_compute_total_costo')

    descripcion = fields.Text(u'Descripción')

    # Agregados del modulo original
    date = fields.Date(string='Fecha',required=True,copy=False,)
    product_id = fields.Many2one(comodel_name='product.product', string='Producto')
    reference = fields.Char(string='Referencia', copy=False,)
    product_qty = fields.Float(string='Cantidad Planificada',copy=False,)
    uom_id = fields.Many2one('uom.uom', string='Uom',)
    cost_price = fields.Float(string='Cost / Unit',copy=False,)

    # actual_quantity = fields.Float(string='Actual Purchased Quantity',compute='_compute_actual_quantity',)
    actual_quantity = fields.Float(string='Cantidad Comprada Actual',)

    hours = fields.Char(string='Horas', required=False)
    actual_timesheet = fields.Char(string='Parte de Horas Actual', required=False)
    basis = fields.Char(string='Base', required=False)

    job_type = fields.Selection(
        selection=[('material', 'Materiales'),
                   ('labour', 'Mano de Obra'),
                   ('overhead', 'Gastos Generales')],
        string="Tipo de Costo",
        required=False,)

    @api.onchange('product_id')
    def _onchan_product_id(self):
        for rec in self:
            rec.descripcion = rec.product_id.name
            rec.product_qty = 1.0
            rec.uom_id = rec.product_id.uom_id.id
            rec.cost_price = rec.product_id.standard_price  # lst_price