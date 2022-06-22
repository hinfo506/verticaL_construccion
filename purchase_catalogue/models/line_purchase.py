from odoo import fields, models, api


class LinePurchase(models.Model):
    _name = 'line.purchase'
    _description = 'Description'
    
    catalogue_id = fields.Many2one(comodel_name='catalogue.catalogue', string='Catalogue_id', required=False)

    item_id = fields.Many2one(comodel_name='item.capitulo', string='Item', required=False)
    amount = fields.Integer(string='Cantidad', required=False)
    amount_available = fields.Integer(string='Cantidad Disponible', required=False)
    amount_total = fields.Integer(string='Cantidad Total', required=False)

    
