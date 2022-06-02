# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.osv import expression

_logger = logging.getLogger(__name__)

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

