# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    standard_picking_type = fields.Many2one('stock.picking.type',
                                            string='Default Picking Type')
    

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    standard_picking_type = fields.Many2one('stock.picking.type',
                                          related='company_id.standard_picking_type',
                                          string='Default Picking Type',
                                          readonly=0)