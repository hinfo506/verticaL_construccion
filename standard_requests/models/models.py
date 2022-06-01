# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.osv import expression

_logger = logging.getLogger(__name__)

READONLY_STATE = {'draft': [('readonly', False)]}


class StandardTags(models.Model):
    _name = 'standard.tags'
    _description = 'Standard Tags'
    _parent_name = 'parent_id'
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    parent_id = fields.Many2one('standard.tags')
    parent_path = fields.Char()
    analytic_id = fields.Many2one('account.analytic.account', string='Cuenta Analitica')
    name = fields.Char('Nombre')
    complete_name = fields.Char(compute='_compute_complete_name', store=1)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for i in self:
            if i.parent_id:
                i.complete_name = '%s/%s' % (
                    i.parent_id.complete_name, i.name)
            else:
                i.complete_name = i.name

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100):
        """ search full """
        args = args or []
        recs = self.browse()
        if not recs:
            domain = ['|', ('name', operator, name), ('complete_name', operator, name)]
            recs = self.search(domain)
        return recs.name_get()
   

class Standard(models.Model):
    _name = 'standard'
    _description = 'Standard'
    _parent_name = 'parent_id'
    _parent_store = True

    name = fields.Char(string='Nombre', required=1)
    parent_id = fields.Many2one('standard', string='Padre')
    line_ids = fields.One2many('standard.line', 'standard_id', copy=True)
    parent_path = fields.Char()
    ref_proyecto = fields.Char('Proyecto')
    ref_etapa  = fields.Char('Etapa')
    is_purchase = fields.Boolean(string='Aparece en Req. Compras')
    is_warehouse = fields.Boolean(string='Aparece en Req. Almacen ')
    

class StandardLine(models.Model):
    _name = 'standard.line'
    _description = 'Standard Line'

    standard_id = fields.Many2one('standard', string='Estandar')
    product_id = fields.Many2one('product.product', string='Producto', required=1)
    uom_id = fields.Many2one('uom.uom', string='Unidad de Medida', required=1)
    qty = fields.Float(string='Cantidad', required=1)

    descripcion = fields.Char(string='Descripcion')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        domain = {}

        if not self.product_id:
            domain['uom_id'] = []

        if not self.uom_id or self.product_id.uom_id.category_id.id \
                != self.uom_id.category_id.id:
            self.uom_id = self.product_id.uom_id.id

        domain['uom_id'] = [('category_id', '=', self.product_id.uom_id.category_id.id)]

        return {'domain': domain}


class StandardRequest(models.Model):
    _name = 'standard.request'
    _description = 'Standard Request'

    name = fields.Char('Codigo', readonly=1)

    standard_id = fields.Many2one('standard', string='Standard', required=1, readonly=1, states=READONLY_STATE)
    tag_id = fields.Many2one('standard.tags', string='Etiqueta', required=1, readonly=1, states=READONLY_STATE)
    line_ids = fields.One2many('standard.request.line', 'request_id', copy=True)
    date = fields.Date('Fecha', default=fields.Date.today())
    date_validation = fields.Datetime('Fecha Validacion', readonly=1)
    state = fields.Selection([
        ('draft','Borrador'),
        ('validate','Validado'),
        ('cancel','Cancelado'),], default='draft', string='Estado')
    note = fields.Text(string='Notes')
    picking_id = fields.Many2one('stock.picking', string='Conduce de Almacen', readonly=1)
    picking_state = fields.Selection(related='picking_id.state')
    partner_id = fields.Many2one('res.partner', 'Contratista')

    def get_standard_lines(self):
        for i in self.line_ids:
            i.unlink()

        lines = []
        for l in self.standard_id.line_ids:
            lines.append((0, 0, {
                'product_id': l.product_id,
                'uom_id': l.uom_id,
                'qty': l.qty,
                'request_id': self.id,
            }))

        self.line_ids = lines

    # @api.multi
    def action_validate(self):
        self.calc_stock()

        i = self.search([
            ('standard_id', '=', self.standard_id.id),
            ('tag_id', '=', self.tag_id.id),
            ('state', '=', 'validate'),
        ])

        if i:
            raise UserError("Ya Este Standard fue solicitado a almacen anteriormente.")

        #if not self.env['res.users'].browse(self._uid).has_group(
        #        'standard_requests.standard_manager'):
        #    for line in self.line_ids:
        #        if line.stock < line.qty:
        #            raise UserError('No puedes Validar la solicitud por falta de Material.')

        requisicion = self.env['purchase.requisition'].search([
            '|',('tag_ids.tag_id', '=', self.tag_id.parent_id.id),
            ('tag_ids.tag_id', '=', self.tag_id.id),
            '|',('standard_id', '=', self.standard_id.parent_id.id),
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

        self.state='validate'
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
        for l in self.line_ids:#.filtered(lambda i: i.request_id.state == 'draft'):
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


class StandardRequestLine(models.Model):
    _name = 'standard.request.line'
    _description = 'Standard Request Line'

    request_id = fields.Many2one('standard.request', string='Peticion')
    product_id = fields.Many2one('product.product', string='Producto')
    uom_id = fields.Many2one('uom.uom', string='Unidad de Medida')
    qty = fields.Float(string='Cantidad')
    qty_done = fields.Float(string='Cantidad Despachada', compute='get_qty_done')
    standard_id = fields.Many2one(related="request_id.standard_id", readonly=1, store=1)
    stock = fields.Float('Stock')
    state = fields.Selection(related="request_id.state", readonly=1, store=1)

    def get_lines(self, picking_id, product_id, lines=[]):
        if picking_id.state == 'done':

            lines.append(
                picking_id.mapped('move_ids_without_package').filtered(
                    lambda r: r.state == 'done'
                    and not r.scrapped
                    and product_id == r.product_id)
                )

            if picking_id.backorder_ids and picking_id.backorder_ids[0].state == 'done':
                self.get_lines(picking_id.backorder_ids[0], product_id, lines, pickings)

        return lines

    @api.depends('request_id.picking_id')
    def get_qty_done(self):
        for line in self:
            lines = []
            picking_lines = self.get_lines(line.request_id.picking_id, line.product_id, lines)

            qty = 0.0
            for move in picking_lines:

                if move.location_dest_id.usage == "customer":
                    if not move.origin_returned_move_id or (
                            move.origin_returned_move_id and move.to_refund):
                        qty += move.product_uom._compute_quantity(move.product_uom_qty, line.uom_id)
                elif move.location_dest_id.usage != "customer" and move.to_refund:
                    qty -= move.product_uom._compute_quantity(move.product_uom_qty, line.uom_id)

            line.qty_done = qty
#pedro sandobal
