from odoo import fields, models


class VerticalItem(models.Model):
    _inherit = "vertical.item"

    standar_id = fields.Many2one(
        comodel_name="standard", string="Standar Relacionado", required=False
    )
