import ast
import json
from collections import defaultdict
from datetime import timedelta, datetime
from random import randint

from odoo import api, Command, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError, AccessError
from odoo.tools import format_amount
from odoo.osv.expression import OR


class Capitulo(models.Model):
    _name = 'capitulo.capitulo'
    _inherit = ['mail.thread','mail.activity.mixin']

    ###### DATOS PRINCIPALES  ########
    number = fields.Char(string='Number', required=True, copy=False, readonly='True',
                         default=lambda self: self.env['ir.sequence'].next_by_code('secuencia.capitulo'))
    numero_capitulo = fields.Char(string='Número Capítulo', required=False)
    name = fields.Char(string='Capitulo', required=True)
    cantidad = fields.Integer('Cantidad')
    total = fields.Float('Importe Total',compute='_compute_total_cap')
    fecha_inicio = fields.Date('Fecha Inicio')
    fecha_finalizacion = fields.Date('Acaba el')

    descripcion = fields.Text('Descripción del Capitulo')
    condicion = fields.Selection(string='Condición', selection=[
        ('presupuestario', 'Presupuestario'),
        ('sobrecoste', 'Sobre Coste'),
        ('adicionales', 'Adicionales'), ],required=False, )

 
    ###### FASES DEL PROYECTO  ########
    project_id = fields.Many2one('project.project', string='Proyecto', required=True)
    fase_principal_id = fields.Many2one(comodel_name='fase.principal', string='Fase Principal', required=True, ondelete='cascade')

    # prueba
    # name_faseini = fields.Char(string='Fase',related="project_id.nombre_fase", required=False)

    subcapitulo_ids = fields.One2many(comodel_name='sub.capitulo', inverse_name='capitulo_id', string='Subcapitulos', required=False)

    ####### CONTADORES  ########
    sub_count = fields.Integer(string='Cantidad Subcapitulos', required=False, compute='subcapitulos_count')
    activi_count = fields.Integer(string='Contador Actividades', compute='get_acti_count')

    @api.onchange('number', 'fase_principal_id')
    def _onchange_join_number_capitulo(self):
        self.numero_capitulo = str(self.fase_principal_id.numero_fase_principal) + "." + str(self.number)

    def subcapitulos_count(self):
        count = self.env['sub.capitulo'].search_count([('capitulo_id', '=', self.id)])
        self.sub_count = count

    def met_subcapitulos(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subcapitulos',
            'res_model': 'sub.capitulo',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.subcapitulo_ids.ids)],
            'context': dict(self._context, default_capitulo_id=self.id),
        }

    def ir_id_capitulo(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Capitulo',
            'res_model': 'capitulo.capitulo',
            'view_mode': 'tree,form',
            'res_id': self.id
        }

    ######################
    #### Actividades #####
    ######################

    def get_acti_count(self):
        for r in self:
            count = self.env['mail.activity'].search_count([('res_id', '=', self.id),('res_model','=','capitulo.capitulo')])
            r.activi_count = count if count else 0

    def met_activi_capitulos(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Actividades',
            'res_model': 'mail.activity',
            'view_mode': 'kanban,tree,form',
            'domain': [('res_id', '=',  self.id),('res_model','=','capitulo.capitulo')],
        }

    def wizard_cambio_precio(self):
        return {
            'name': 'Cambiar Precio Masivo desde Capitulo',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cambio.precio',
            'context': {
                'default_capitulo_id': self.id,
                'default_is_vacio': '1',
                # 'default_nuevo_precio': '70',
                'default_info': "LOS PRECIOS SERAN CAMBIADOS A PARTIR DE </br><strong>"+str(self.project_id.name)+"/"+str(self.fase_principal_id.name)+"/"+str(self.name)+" :</strong>",
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        record = super(Capitulo, self).copy(default)
        for subcapitulo in self.subcapitulo_ids:
            record.subcapitulo_ids |= subcapitulo.copy()

        return record

    def _compute_total_cap(self):
        for record in self:
            suma = 0.0
            for sub in record.subcapitulo_ids:
                suma += sub.total
            record.update({'total': suma, })

    #####################################
    ## Onchange para Agregar Las Fases ##
    #####################################
    @api.onchange('project_id')
    def _onchange_domain_project(self):
        fase = {}
        fase['domain'] = {'fase_principal_id': [('project_id', '=', self.project_id.id)]}
        return fase
