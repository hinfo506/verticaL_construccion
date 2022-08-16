from odoo import fields, models


class View(models.Model):
    _inherit = "ir.ui.view"

    type = fields.Selection(
        selection_add=[("project_stage_item", "Project-Stage-Item View")]
    )
