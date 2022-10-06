from odoo import fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    stage_id = fields.Many2one(comodel_name='vertical.stage', string='Fase', required=False)
    project_id = fields.Many2one(related='stage_id.project_id', string='Proyecto', required=False)

    # MOdificando metod para confirmar la compra
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
                    'amount_confirm': line.product_qty,
                    'purchase_stage': 'confirm'
                })
            ################################

        return True

    def button_cancel(self):
        for order in self:
            for move in order.order_line.mapped('move_ids'):
                if move.state == 'done':
                    raise UserError(
                        _('Unable to cancel purchase order %s as some receptions have already been done.') % (
                            order.name))
            # If the product is MTO, change the procure_method of the closest move to purchase to MTS.
            # The purpose is to link the po that the user will manually generate to the existing moves's chain.
            if order.state in ('draft', 'sent', 'to approve', 'purchase'):
                for order_line in order.order_line:
                    order_line.move_ids._action_cancel()
                    if order_line.move_dest_ids:
                        move_dest_ids = order_line.move_dest_ids
                        if order_line.propagate_cancel:
                            move_dest_ids._action_cancel()
                        else:
                            move_dest_ids.write({'procure_method': 'make_to_stock'})
                            move_dest_ids._recompute_state()

            for pick in order.picking_ids.filtered(lambda r: r.state != 'cancel'):
                pick.action_cancel()

            order.order_line.write({'move_dest_ids': [(5, 0, 0)]})

            ###########################################
            for line in order.order_line:
                item = self.env['vertical.item'].search([('id', '=', line.item_id.id)])
                amount = item.amount_confirm - line.product_qty
                # raise ValidationError(amount_cancel)
                item.update({
                    'amount_confirm': amount,
                    'purchase_stage': 'earring' if amount == 0 else 'qty_earring'
                })
            #############################################

        return super(PurchaseOrder, self).button_cancel()

    # def button_cancel(self):
    #     for order in self:
    #         for inv in order.invoice_ids:
    #             if inv and inv.state not in ('cancel', 'draft'):
    #                 raise UserError(_("Unable to cancel this purchase order. You must first cancel the related vendor bills."))
    #
    #     self.write({'state': 'cancel', 'mail_reminder_confirmed': False})
