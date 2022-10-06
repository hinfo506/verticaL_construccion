# -*- coding: utf-8 -*-

from odoo import models, fields, api

class VerticalCostAnalysis(models.Model):
    _name = 'vertical.cost.analysis'

    name = fields.Char('Nombre')
    standard_id = fields.Many2one(comodel_name='standard', string='Standard')

    stage_ids = fields.One2many(comodel_name='vertical.stage', inverse_name='cost_analysis_id', string='Stage_id', required=False)

    items_ids = fields.One2many(comodel_name='vertical.item', inverse_name='cost_analysis_id', string='Items_ids', required=False)

    list_ids = fields.Many2many(comodel_name='standard.line', string='List_ids')

    @api.onchange('standard_id')
    def _onchange_list_ids(self):
        for record in self:
            if record.standard_id:
                data = [('standard_id', '=', record.standard_id.id)]
                line = self.env['standard.line'].search(data)
                record.list_ids = line

    # Revisar esto
    # @api.onchange('standard_id')
    # def _onchange_standard_list(self):
    #     for record in self:
    #         if record.standard_id:
    #             data = [('standard_id', '=', record.standard_id.id)]
    #             line = self.env['standard.line'].search(data)
    #             record.list_ids = line