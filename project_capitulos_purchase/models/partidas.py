# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Partidas(models.Model):
    _inherit = 'partidas.partidas'

    purchase_order_ids = fields.One2many(comodel_name='purchase.order', inverse_name='partida_id', string='Purchase_order_ids', required=False)
    it_was_bought = fields.Boolean(string='It_was_bought', required=False, default=False)

    def execute_purchase(self):
        contactos = self.env['res.partner'].search([])
        # raise ValidationError(self.item_capitulo_ids)

        purchase = self.env['purchase.order'].create({
            'partner_id': contactos[0].id,
            'partida_id': self.id,
        })

        for i in self.item_capitulo_ids:
            purchase_line = self.env['purchase.order.line'].create({
                'order_id': purchase.id,
                'product_id': i.product_id.id,
                'name': i.descripcion,
                'price_unit': i.cost_price,
                'product_qty': i.product_qty,
            })
        self.it_was_bought = True


