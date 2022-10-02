from odoo import fields, models, api


class VerticalLineCatalogue(models.Model):
    _name = 'vertical.line.catalogue'

    name = fields.Char()

    catalogue_id = fields.Many2one(comodel_name='vertical.catalogue', string='Catalogue_id', required=False)
