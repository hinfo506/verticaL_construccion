from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError,RedirectWarning

class Subcapitulo(models.Model):
    _name = 'sub.capitulo'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ###### DATOS PRINCIPALES  ########
    number = fields.Char(string='Number', required=True, copy=False, readonly='True',
                       default=lambda self: self.env['ir.sequence'].next_by_code('secuencia.subcapitulo'))
    numero_subcapitulo = fields.Char(string='Número Subcapítulo', required=False)
    name = fields.Char(string='Subcapítulo', required=True)
    descripcion = fields.Text('Descripción del Subcapítulo')
    cantidad = fields.Integer('Cantidad')
    total = fields.Float('Importe Total')
    fecha_inicio = fields.Date('Fecha Inicio')
    fecha_finalizacion = fields.Date('Acaba el')

    condicion = fields.Selection(string='Condición', selection=[
        ('presupuestario', 'Presupuestario'),
        ('sobrecoste', 'Sobre Coste'),
        ('adicionales', 'Adicionales'), ], required=False, )

    ###### FASES DEL PROYECTO  ########
    project_id = fields.Many2one('project.project', string='Proyecto')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo',ondelete='cascade')
    subcapitulo_ids = fields.One2many(comodel_name='item.capitulo', inverse_name='subcapitulo_id', string='Subcapitulo', required=False)
    fase_principal_id = fields.Many2one(comodel_name='fase.principal',string='Fase Principal', required=False)
    # fase_principal_id = fields.Many2one(related='capitulo_id.fase_principal_id', string='Fase Principal', required=False)

    ###### CONTADORES  ########
    partidas_ids = fields.One2many(comodel_name='partidas.partidas',inverse_name='subcapitulo_id', string='Partidas id', required=False)
    partidas_count = fields.Integer(string='Contador Item', compute='get_partidas_count')
    activ_count = fields.Integer(string='Contador actividades', compute='get_acts_count')

    @api.onchange('number', 'capitulo_id')
    def _onchange_join_number(self):
        self.numero_subcapitulo = str(self.capitulo_id.numero_capitulo) + "." + str(self.number)

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


    def get_partidas_count(self):
        for r in self:
            r.partidas_count = self.env['partidas.partidas'].search_count([('subcapitulo_id', '=',  self.id)])

    ###############
    # Actividades #
    ###############


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
        }

    def action_view_partidas(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Partidas',
            'res_model': 'partidas.partidas',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.partidas_ids.ids)],
            'context': dict(self._context, default_subcapitulo_id=self.id),
        }

    def wizard_cambio_precio(self):
        return {
            'name': 'Cambiar Precio Masivo desde Subcapitulo',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cambio.precio',
            'context': {
                'default_is_vacio': True,
                'default_subcapitulo_id': self.id,
                'default_info': "LOS PRECIOS SERAN CAMBIADOS A PARTIR DE </br>" + "<strong>"+ str(self.capitulo_id.project_id.name)+"/"+str(self.capitulo_id.name)+"/" + str(self.name) + " :</strong>",
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        # if self.partidas_ids:
        #     default['partidas_ids'] = self.partidas_ids.copy().ids // esto no borrar me queda de ejemplo para la eternidad

        record = super(Subcapitulo, self).copy(default)
        for partida in self.partidas_ids:
            record.partidas_ids |= partida.copy()

        return record

