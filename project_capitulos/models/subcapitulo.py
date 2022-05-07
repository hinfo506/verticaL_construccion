from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError,RedirectWarning

class Subcapitulo(models.Model):
    _name = 'sub.capitulo'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Subcapítulo', required=True)
    descripcion = fields.Text('Descripción del Subcapítulo')
    cantidad = fields.Integer('Cantidad')
    total = fields.Float('Importe Total')
    fecha_inicio = fields.Date('Fecha Inicio')
    fecha_finalizacion = fields.Date('Acaba el')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo')

    number = fields.Char(string='Number', required=True, copy=False, readonly='True',
                       default=lambda self: self.env['ir.sequence'].next_by_code('secuencia.subcapitulo'))
    
    numero_subcapitulo = fields.Char(string='Número Subcapítulo', required=False)

    @api.onchange('number','capitulo_id')
    def _onchange_join_number(self):
        self.numero_subcapitulo = str(self.capitulo_id.numero_capitulo) + "." + str(self.number)

    # material_total = fields.Float(string='Total Coste Materiales', compute='_amount_all' ,readonly='True')
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

    partidas_ids = fields.One2many(comodel_name='partidas.partidas',inverse_name='subcapitulo_id', string='Partidas id', required=False)

    # item_capitulo_materiales_ids = fields.One2many(
    #     comodel_name='item.capitulo',
    #     inverse_name='subcapitulo_id',
    #     string='Materiales',
    #     domain=[('job_type', '=', 'material')],
    # )
    # item_mano_obra_ids = fields.One2many(
    #     comodel_name='item.capitulo',
    #     inverse_name='subcapitulo_id',
    #     string='Mano de Obra',
    #     domain=[('job_type', '=', 'labour')],
    # )
    # item_capitulo_gastos_generales = fields.One2many(
    #     comodel_name='item.capitulo',
    #     inverse_name='subcapitulo_id',
    #     string='Gastos Generales',
    #     copy=False,
    #     domain=[('job_type', '=', 'overhead')],
    # )
    #
    # item_capitulo_maquinaria = fields.One2many(
    #     comodel_name='item.capitulo',
    #     inverse_name='subcapitulo_id',
    #     string='Maquinaria',
    #     domain=[('job_type', '=', 'machinery')],
    # )
    #
    partidas_count = fields.Integer(string='Contador Item', compute='get_partidas_count')

    def get_partidas_count(self):
        for r in self:
            r.partidas_count = self.env['partidas.partidas'].search_count([('subcapitulo_id', '=',  self.id)])

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

    def action_view_partidas(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Partidas',
            'res_model': 'partidas.partidas',
            'view_mode': 'tree,form',
            'domain': [('subcapitulo_id', '=',  self.id)],
            # 'views': [(self.env.ref('project_capitulos.itemsubcapitulo_view_tree').id, 'tree'), (self.env.ref('project_capitulos.itemsubcapitulo_view_form').id, 'form')],
            'context': dict(self._context, default_subcapitulo_id=self.id),
        }

    # def action_view_item(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Items',
    #         'res_model': 'item.capitulo',
    #         'view_mode': 'tree,form',
    #         'domain': [('subcapitulo_id', '=',  self.id)],
    #         'views': [(self.env.ref('project_capitulos.itemsubcapitulo_view_tree').id, 'tree'), (self.env.ref('project_capitulos.itemsubcapitulo_view_form').id, 'form')],
    #         'context': dict(self._context, default_subcapitulo_id=self.id),
    #     }

