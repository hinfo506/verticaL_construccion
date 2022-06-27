from odoo import fields, models, api
from odoo.exceptions import ValidationError
from collections import defaultdict

class LinePurchase(models.Model):
    _name = 'line.purchase'
    _description = 'Description'
    
    catalogue_id = fields.Many2one(comodel_name='catalogue.catalogue', string='Catalogue_id', required=False)

    item_id = fields.Many2one(comodel_name='item.capitulo', string='Item', required=False, context="{'group_by':'product_id.id'}")
    amount = fields.Integer(string='Cantidad', required=False)
    amount_available = fields.Integer(string='Cantidad Disponible', required=False)
    amount_total = fields.Integer(string='Cantidad Total', required=False)

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product_id',
        required=False)

    @api.onchange('item_id')
    def _onchange_domain_project(self):
        if self.catalogue_id.project_id:
            # raise ValidationError(self.catalogue_id.project_id.id)
            res = {}
            res['domain'] = {'item_id': [('project_id', '=', self.catalogue_id.project_id.id)]}
            # raise ValidationError(res)
            # res['context'] = {'group_by': 'product_id'}
            online_partner = self.env['item.capitulo'].search([('project_id', '=', self.catalogue_id.project_id.id)]).mapped("product_id")

            # online_partner = self.env['res.users'].search([]).filtered(lambda x: x.im_status == 'online').mapped(
            #     "partner_id").ids
            # list=[]
            # for l in online_partner:
            #     # ks_dashboard_data.append(dashboard_data)
            #     list.append(l.name)
            # raise ValidationError(list)
            res = online_partner
            return res
        else:
            raise ValidationError('Debe seleccionar un Proyecto')
