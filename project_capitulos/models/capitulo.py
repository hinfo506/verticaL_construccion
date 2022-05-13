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

    name = fields.Char(string='Capitulo', required=True)
    numero_capitulo = fields.Char(string=u'Número capítulo', readonly=True, default='New')

    @api.model
    def create(self,vals):
        if vals.get('numero_capitulo','1') == '1':
            vals['numero_capitulo'] = self.env['ir.sequence'].next_by_code('secuencia.capitulo') or '1'
        result = super(Capitulo, self).create(vals)
        return result


    cantidad = fields.Integer('Cantidad')
    total = fields.Float('Importe Total')
    fecha_inicio = fields.Date('Fecha Inicio')
    fecha_finalizacion = fields.Date('Acaba el')
    project_id = fields.Many2one('project.project', string='Proyecto')
    descripcion = fields.Text('Descripción del Capitulo')
    sub_count = fields.Integer(string='Cantidad Subcapitulos', required=False,compute='subcapitulos_count')
    subcapitulo_ids = fields.One2many(
        comodel_name='sub.capitulo',
        inverse_name='capitulo_id',
        string='Subcapitulos',
        required=False)

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
    activi_count = fields.Integer(string='Contador Actividades', compute='get_acti_count')

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
                'default_is_vacio': True,
                'default_info': "LOS PRECIOS SERAN CAMBIADOS A PARTIR DE AQUI EN ADELANTE: <strong>CAPITULO/SUBCAPITULO/PARTIDA</strong>",
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }