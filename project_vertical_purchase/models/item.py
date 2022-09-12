from odoo import fields, models, api
from odoo.exceptions import ValidationError

class VerticalItem(models.Model):
    _inherit = 'vertical.item'
    
    amount_confirm = fields.Float(string='Amount_confirm', required=False)
    amount_delivered = fields.Float(string='Amount_delivered', required=False)

    # def purchase_from_item(self):
    #     act_ids = self.env.context.get('active_ids')
    #     item_ids = self.env['vertical.item'].search([('id', '=', act_ids)])
    #     # raise ValidationError(item_ids[0].vertical_stage_id)
    #     #
    #     # for i in item_ids:
    #     #     if i.stage_id != item_ids[0].stage_id:
    #     #         pass
    #
    #     purchase = self.env['purchase.order'].create({
    #         'partner_id': self.env.user.id,
    #         'stage_id': item_ids[0].vertical_stage_id.id,
    #     })
    #     for i in item_ids:
    #         # for i in item.item_ids:
    #         purchase_line = self.env['purchase.order.line'].create({
    #             'order_id': purchase.id,
    #             'product_id': i.product_id.id,
    #             'name': 'esta es la descripcion',
    #             'product_qty': i.product_qty,
    #             'price_unit': i.cost_price,
    #             'item_id': i.id,
    #         })


    def purchase_from_item(self):
        act_ids = self.env.context.get('active_ids')
        item_ids = self.env['vertical.item'].search([('id', '=', act_ids)])
        # raise ValidationError(item_ids[0].vertical_stage_id)
        #
        # for i in item_ids:
        #     if i.stage_id != item_ids[0].stage_id:
        #         pass

        # purchase = self.env['purchase.order'].create({
        #     'partner_id': self.env.user.id,
        #     'stage_id': item_ids[0].vertical_stage_id.id,
        # })
        # product.template

        data = []
        for i in item_ids:
            data += i.product_id.seller_ids.name

        raise ValidationError(data)
