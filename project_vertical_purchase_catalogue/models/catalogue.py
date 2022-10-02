# -*- coding: utf-8 -*-

from odoo import models, fields, api

class VerticalCatalogue(models.Model):
    _name = 'vertical.catalogue'

    name = fields.Char('Name')

    line_catalogue_ids = fields.One2many(
        comodel_name='vertical.line.catalogue',
        inverse_name='catalogue_id',
        string='Line_catalogue_ids',
        required=False)
