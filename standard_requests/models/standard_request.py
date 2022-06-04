# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.osv import expression

_logger = logging.getLogger(__name__)

READONLY_STATE = {'draft': [('readonly', False)]}

class StandardRequest(models.Model):
    _name = 'standard.request'
    _description = 'Standard Request'

    name = fields.Char('Codigo', readonly=1)

    # standard_id = fields.Many2one('standard', string='Standard', required=1, readonly=1, states=READONLY_STATE)
    standard_id = fields.Many2one('standard', string='Standard', required=1)
    # tag_id = fields.Many2one('standard.tags', string='Etiqueta', required=1, readonly=1, states=READONLY_STATE)
    line_ids = fields.One2many('standard.request.line', 'request_id', copy=True)
    date = fields.Date('Fecha', default=fields.Date.today())
    date_validation = fields.Datetime('Fecha Validacion', readonly=1)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('validate', 'Validado'),
        ('cancel', 'Cancelado'), ], default='draft', string='Estado')
    note = fields.Text(string='Notes')
    # picking_id = fields.Many2one('stock.picking', string='Conduce de Almacen', readonly=1)
    # picking_state = fields.Selection(related='picking_id.state')
    # partner_id = fields.Many2one('res.partner', 'Contratista')

    # Fases
    project_id = fields.Many2one(comodel_name='project.project', string='Proyecto', required=False)
    fase_principal_id = fields.Many2one(comodel_name='fase.principal', string='Fase Principal', required=False)
    capitulo_id = fields.Many2one(comodel_name='capitulo.capitulo', string='Capitulo', required=False)
    subcapitulo_id = fields.Many2one(comodel_name='sub.capitulo', string='Subcapitulo', required=False)

    @api.onchange('project_id')
    def _onchange_credencial_asignada(self):
        fase = {}
        fase['domain'] = {'fase_principal_id': [('project_id', '=', self.project_id.id)]}
        return fase

    @api.onchange('fase_principal_id')
    def _onchange_credencial_asignada(self):
        cap = {}
        cap['domain'] = {'capitulo_id': [('fase_principal_id', '=', self.fase_principal_id.id)]}
        return cap

    @api.onchange('capitulo_id')
    def _onchange_credencial_asignada(self):
        sub = {}
        sub['domain'] = {'subcapitulo_id': [('capitulo_id', '=', self.capitulo_id.id)]}
        return sub

    def get_standard_lines(self):
        for i in self.line_ids:
            i.unlink()

        lines = []

        for l in self.standard_id.line_ids:
            lines.append((0, 0, {
                'product_id': l.product_id.id,
                'uom_id': l.uom_id.id,
                'qty': l.qty,
                'request_id': self.id,
            }))

        self.line_ids = lines

    # @api.multi
    def action_validate(self):
        self.calc_stock()

        i = self.search([
            ('standard_id', '=', self.standard_id.id),
            ('state', '=', 'validate'),
        ])

        if i:
            raise UserError("Ya Este Standard fue solicitado a almacen anteriormente.")

        # if not self.env['res.users'].browse(self._uid).has_group(
        #        'standard_requests.standard_manager'):
        #    for line in self.line_ids:
        #        if line.stock < line.qty:
        #            raise UserError('No puedes Validar la solicitud por falta de Material.')

        requisicion = self.env['purchase.requisition'].search([
            '|', ('tag_ids.tag_id', '=', self.tag_id.parent_id.id),
            ('tag_ids.tag_id', '=', self.tag_id.id),
            '|', ('standard_id', '=', self.standard_id.parent_id.id),
            ('standard_id', '=', self.standard_id.id)
        ])

        _logger.info(requisicion)

        if not requisicion:
            raise UserError('No se a realizado la requisicion de compras de este Standard para este proyecto.')

        picking_type_id = self.env.user.company_id.standard_picking_type
        orig_id = picking_type_id.default_location_src_id.id
        dest_id = self.env.ref("stock.stock_location_customers").id

        if not orig_id:
            raise UserError('Debe de configurar el almacen correspondiente en el Menu Configuraciones/Settings.')

        move_ids = []
        for i in self.line_ids:
            move_ids.append((
                0, 0, {
                    'name': i.product_id.name,
                    'product_id': i.product_id.id,
                    'product_uom_qty': i.qty,
                    'product_uom': i.uom_id.id,
                    'location_id': orig_id,
                    'location_dest_id': dest_id,
                }
            ))

        note = """
        Proyecto: {}

        {}
        """.format(self.tag_id.name, self.note or '')

        analytic_id = self.tag_id.analytic_id.id or self.tag_id.parent_id.analytic_id.id

        self.picking_id = self.env['stock.picking'].create({
            'picking_type_id': picking_type_id.id,
            'location_id': orig_id,
            'partner_id': self.partner_id.id,
            'location_dest_id': dest_id,
            'origin': self.name,
            'move_ids_without_package': move_ids,
            'note': note,
            'x_studio_field_analytic_account_id': analytic_id,
            'x_studio_projecto': self.tag_id.display_name,
        }).id

        self.state = 'validate'
        self.date_validation = fields.Datetime.now()

    # @api.multi
    def action_cancel(self):
        if self.picking_id.state == 'done':
            raise UserError('No se puede cancelar ya que Almacen Despacho las Mercancias')

        self.picking_id.action_cancel()
        self.state = 'cancel'

    # @api.multi
    def calc_stock(self):
        tag_id = self.tag_id
        tag_and_parent = [tag_id.id, tag_id.parent_id.id]
        data = {}
        for l in self.line_ids:  # .filtered(lambda i: i.request_id.state == 'draft'):
            l.stock = l.product_id.qty_available
        #    tag_ids = self.env['standard.tags'].search(
        #        ['|', '|',
        #         ('id', '=', tag_id.id),
        #         ('parent_id', '=', tag_id.id),
        #         ('parent_id.parent_id', '=', tag_id.id)])

        #    consumidos = self.env['standard.request.line'].search([
        #        ('request_id.tag_id', 'in', tag_ids.ids),
        #        ('request_id.state', '=', 'validate'),
        #        ('product_id', '=', l.product_id.id),
        #    ])

        #    for i in consumidos:
        #        data.setdefault(i.product_id.id, {'consumido': 0, 'comprado': 0})
        #        data[i.product_id.id]['consumido'] += i.qty_done

        #
        #    # requisiciones que tienen orden de compras
        #    requisiciones = self.env['purchase.requisition'].search([
        #        ('tag_ids.tag_id', 'in', tag_ids.ids)#, tag_ids.parent_id.id, tag_ids.parent_id.parent_id.id)),
        #    ]).filtered(lambda r: r.purchase_ids)

        #    _logger.info(('requisiciones', requisiciones, tag_ids, tag_ids.ids))
        #    comprados = []
        #
        #    for req in requisiciones:
        #        req.get_product_qty_receive()
        #
        #        for line in req.distribution_ids.filtered(lambda r: r.product_id.id == l.product_id.id):
        #            if line.tag_id.id in tag_and_parent:
        #                data.setdefault(line.product_id.id, {'consumido': 0, 'comprado': 0})
        #                data[line.product_id.id]['comprado'] += line.product_qty_receive

        #    data.setdefault(l.product_id.id, {'consumido': 0, 'comprado': 0})
        #    l.stock = data[l.product_id.id]['comprado'] - data[l.product_id.id]['consumido']

    @api.model
    def create(self, vals):
        standard_id = self.env['standard'].browse(vals['standard_id'])
        lines = []
        for l in standard_id.line_ids:
            lines.append((0, 0, {
                'product_id': l.product_id.id,
                'uom_id': l.uom_id.id,
                'qty': l.qty,
                'request_id': self.id,
            }))

        vals['line_ids'] = lines
        vals['name'] = self.env['ir.sequence'].next_by_code('standard.requests')

        return super(StandardRequest, self).create(vals)

    def unlink(self):
        for i in self:
            if i.state == 'validate':
                raise UserError('Solo puede Eliminar una orden si esta en estado Borrador o Cancelado.')

        return super(StandardRequest, self).unlink()

    def action_guardar(self):
        pass