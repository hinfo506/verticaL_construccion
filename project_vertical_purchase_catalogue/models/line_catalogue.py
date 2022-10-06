from odoo import fields, models


class VerticalLineCatalogue(models.Model):
    _name = "vertical.line.catalogue"

    name = fields.Char(string="Nombre")
    catalogue_id = fields.Many2one(
        comodel_name="vertical.catalogue", string="Catalogue_id", required=False
    )
