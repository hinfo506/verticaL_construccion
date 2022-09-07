from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    stage_id = fields.Many2one(comodel_name='vertical.stage', string='Stage_id', required=False)

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])

            ###############################
            for line in order.order_line:
                item = self.env['vertical.item'].search([('id', '=', line.item_id.id)])
                # raise ValidationError(item)
                # line.stage_id
                item.update({
                    'amount_confirm': line.product_qty
                })
            ################################

        return True

        # Mi modificacion
        # self.env['vertical.item'].search([('id', '=', id_location)])
        # for order in self:
        #     for line in order.order_line:
        #         item = self.env['vertical.item'].search([('id', '=', line.stage_id.id)])
        #         raise ValidationError(item)
        #         # line.stage_id
        #         item.update({
        #             'amount_confirm': line.product_qty
        #         })
