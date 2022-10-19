# -*- coding: utf-8 -*-

import logging
from odoo import models, fields
_logger = logging.getLogger(__name__)


class StandardLine(models.Model):
    _name = "standard.line"
    _inherit = "item.item"
    _description = "Standard Line"

    standard_id = fields.Many2one("standard", string="Estandar")
