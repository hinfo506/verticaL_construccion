# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class VerticalStage(models.Model):
    _inherit = 'vertical.stage'

    def purchase_from_stage(self):
        act_ids = self.env.context.get('active_ids')
        stage_ids = self.env['vertical.stage'].search([('id', '=', act_ids)])
        # uid = self.env.user
        # raise ValidationError(uid)
        for stage in stage_ids:
            purchase = self.env['purchase.order'].create({
                'partner_id': self.env.user.id,
                'stage_id': stage.id,
            })
            for i in stage.item_ids:
                purchase_line = self.env['purchase.order.line'].create({
                    'order_id': purchase.id,
                    'product_id': i.product_id.id,
                    'name': 'esta es la descripcion',
                    'product_qty': i.product_qty,
                    'price_unit': i.cost_price,
                    'item_id': i.id,
                })
