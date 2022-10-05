from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    item_id = fields.Many2one(comodel_name='vertical.item', string='Item_id', required=False)
