# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class StandardTags(models.Model):
    _name = 'standard.tags'
    _description = 'Standard Tags'
    _parent_name = 'parent_id'
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'
    #
    # parent_id = fields.Many2one('standard.tags')
    parent_id = fields.Many2one('standard.tags',index=True,ondelete='cascade', readonly=True)
    # parent_path = fields.Char()
    parent_path = fields.Char(index=True)
    analytic_id = fields.Many2one('account.analytic.account', string='Cuenta Analitica')
    name = fields.Char('Nombre')
    complete_name = fields.Char(compute='_compute_complete_name', store=1)



    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for i in self:
            if i.parent_id:
                i.complete_name = '%s/%s' % (
                    i.parent_id.complete_name, i.name)
            else:
                i.complete_name = i.name

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100):
    #     """ search full """
    #     args = args or []
    #     recs = self.browse()
    #     if not recs:
    #         domain = ['|', ('name', operator, name), ('complete_name', operator, name)]
    #         recs = self.search(domain)
    #     return recs.name_get()