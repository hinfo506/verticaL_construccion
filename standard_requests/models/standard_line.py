# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.osv import expression

_logger = logging.getLogger(__name__)

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