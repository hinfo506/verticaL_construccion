from odoo import fields, models, api


class VerticalLineCatalogue(models.Model):
    _name = 'vertical.line.catalogue'

    name = fields.Char()

    product_id = fields.Many2one(comodel_name='product.product', string='Product_id')
    qty = fields.Float(string='Cantidad', required=False)

    catalogue_id = fields.Many2one(comodel_name='vertical.catalogue', string='Catalogue_id', required=False)
