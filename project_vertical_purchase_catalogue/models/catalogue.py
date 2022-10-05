# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class VerticalCatalogue(models.Model):
    _name = 'vertical.catalogue'

    name = fields.Char('Name')

    project_id = fields.Many2one(comodel_name='project.project', string='Project_id', required=False)
    item_ids = fields.Many2many(comodel_name='vertical.item', string='Item_ids')
    line_catalogue_ids = fields.One2many(comodel_name='vertical.line.catalogue', inverse_name='catalogue_id', string='Line_catalogue_ids', required=False)
    product_ids = fields.Many2many(comodel_name='product.product', string='Product_ids')

    @api.onchange('project_id')
    def onchange_project(self):
        for record in self:
            # data=[]
            data = [('project_id', '=', record.project_id.id)]
            if record.project_id:
                data = [('project_id', '=', record.project_id.id)]
            items = self.env['vertical.item'].search(data)
            record.item_ids = items
            record.product_ids = items.mapped("product_id")
            # raise ValidationError(items.mapped("product_id"))
            record.line_catalogue_ids = []
            record.create_line(items.mapped("product_id"))

    def create_line(self,product_list):
        # raise ValidationError(product_list)
        for record in self:
            for p in product_list:
                items = self.env['vertical.item'].search([('product_id', '=', p.id)])
                suma = 0.0
                for i in items:
                    suma += i.product_qty
                current = self.env['vertical.line.catalogue'].create({
                    'product_id': p.id,
                    'qty': suma,
                    'catalogue_id': record.id,
                })

