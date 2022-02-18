from odoo import fields, models, api
# import logging
# import pytz
# import threading
# from collections import OrderedDict, defaultdict
# from datetime import date, datetime, timedelta
# from psycopg2 import sql
#
# from odoo import api, fields, models, tools, SUPERUSER_ID
# from odoo.addons.iap.tools import iap_tools
# from odoo.addons.mail.tools import mail_validation
# from odoo.addons.phone_validation.tools import phone_validation
# from odoo.exceptions import UserError, AccessError
# from odoo.osv import expression
# from odoo.tools.translate import _
# from odoo.tools import date_utils, email_re, email_split, is_html_empty

# from . import crm_stage

# _logger = logging.getLogger(__name__)

class Subcapitulo(models.Model):
    _name = 'sub.capitulo'

    name = fields.Char(string='Sub-Capitulo', required=True)
    descripcion = fields.Text('Descripción del Sub-Capitulo')
    total = fields.Float('Importe Total')
    fecha_finalizacion = fields.Date('Fecha Finalización')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo')

    number = fields.Char(string='Number', required=True, copy=False,
                       default=lambda self: self.env['ir.sequence'].next_by_code('task.lfpv'))

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
    item_capitulo_fastos_generales = fields.One2many(
        comodel_name='item.capitulo',
        inverse_name='subcapitulo_id',
        string='Gatos Generales',
        copy=False,
        domain=[('job_type', '=', 'overhead')],
    )


class ItemCapitulo(models.Model):
    _name = 'item.capitulo'

    name = fields.Char(string='Sub-Capitulo', required=True)
    descripcion = fields.Text('Descripción del Sub-Capitulo')
    total = fields.Float('Importe Total')
    fecha_finalizacion = fields.Date('Fecha Finalización')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo')
    subcapitulo_id = fields.Many2one('sub.capitulo', string='Capitulo')

    job_type = fields.Selection(
        selection=[('material', 'Materiales'),
                   ('labour', 'Mano de Obra'),
                   ('overhead', 'Gastos Generales')],
        string="Tipo de Costo",
        required=False,
    )
