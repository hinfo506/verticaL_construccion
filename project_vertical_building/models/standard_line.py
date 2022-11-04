import logging
from odoo import fields, models
_logger = logging.getLogger(__name__)


class StandardLine(models.Model):
    _name = "standard.line"
    _inherit = "item.item"
    _description = "Standard Line"

    standard_id = fields.Many2one("standard", string="Estandar")
