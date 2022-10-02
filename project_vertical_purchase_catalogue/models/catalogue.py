# -*- coding: utf-8 -*-

from odoo import models, fields, api

class VerticalCatalogue(models.Model):
    _name = 'vertical.catalogue'

    name = fields.Char('Name')
