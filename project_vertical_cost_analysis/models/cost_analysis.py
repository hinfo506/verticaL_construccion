# -*- coding: utf-8 -*-

from odoo import models, fields, api

class VerticalCostAnalysis(models.Model):
    _name = 'vertical.cost.analysis'

    name = fields.Char('Nombre')
    standard_id = fields.Many2one(comodel_name='standard', string='Standard')

    stage_ids = fields.One2many(comodel_name='vertical.stage', inverse_name='cost_analysis_id', string='Stage_id', required=False)
