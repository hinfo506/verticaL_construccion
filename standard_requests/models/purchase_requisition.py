# -*- coding: utf-8 -*-

import logging
import copy
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    standard_id = fields.Many2one('standard', string='Standard')
    tag_ids = fields.One2many('standard.requisition', 'requisition_id', string='Etiquetas Proyectos')
    distribution_ids = fields.One2many('standard.distribution', 'requisition_id')

    # @api.multi
    def action_set_standard(self):
        self.line_ids.unlink()
        self.distribution_ids.unlink()
        temp = []
        lines = []
        for i in self.standard_id.line_ids:
            qty = i.qty * len(self.tag_ids) if self.tag_ids else i.qty
            lines.append((0, 0, {
                'product_id': i.product_id.id,
                'product_uom_id': i.uom_id.id,
                'name': i.descripcion,
                'product_qty': qty,
            }))

            temp.append({
                'product_id': i.product_id.id,
                'product_qty': i.qty,
                'tag_id':False,
            })

        line_distribution = []
        for l in temp:
            for line in self.tag_ids:

                d = copy.deepcopy(l)
                d.update({'tag_id': line.tag_id.id})
                
                line_distribution.append((0, 0, d))

        self.line_ids = lines
        self.distribution_ids = line_distribution

    def get_product_qty_receive(self):
        for rec in self:
            temp = {}
            for purchase in rec.purchase_ids:
                for l in purchase.order_line:
                    temp.setdefault(l.product_id.id, 0)
                    temp[l.product_id.id] += l.qty_received

            update_dist = []
            for dist in rec.distribution_ids:
                product_id = dist.product_id.id

                if not temp.get(product_id, 0):
                    continue

                if dist.product_qty >= temp.get(product_id, 0):
                    update_dist.append((1, dist.id, {'product_qty_receive': temp.get(product_id)}))
                    temp[product_id] = 0

                elif dist.product_qty < temp.get(product_id, 0):
                    update_dist.append((1, dist.id, {'product_qty_receive': dist.product_qty}))
                    temp[product_id] -= dist.product_qty

            rec.distribution_ids = update_dist


class StandardDistribution(models.Model):
    _name = 'standard.distribution'

    requisition_id = fields.Many2one('purchase.requisition')
    product_id = fields.Many2one('product.product')
    product_qty = fields.Float(string='Cant. Comprada')
    product_qty_receive = fields.Float('Cant. Recibida')
    tag_id = fields.Many2one('standard.tags', string='Proyecto')

class StandardRequisition(models.Model):
    _name = 'standard.requisition'

    name = fields.Char(related="tag_id.display_name")
    requisition_id = fields.Many2one('purchase.requisition')
    tag_id = fields.Many2one('standard.tags', 'Proyecto')
