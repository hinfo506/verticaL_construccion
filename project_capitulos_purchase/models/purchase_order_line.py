from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order"

    partida_id = fields.Many2one(
        comodel_name="partidas.partidas", string="Partida_id", required=False
    )
