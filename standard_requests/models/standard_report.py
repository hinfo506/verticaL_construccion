# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StandardRequestReport(models.TransientModel):
    _name = 'standard.request.report'

    tag_id = fields.Many2one('standard.tags', string='Etiqueta Proyecto')

    def get_tag_info(self, tag):
        if not self.tag_id:
            raise UserError('Debe de indicar una Etiqueta/Proyecto')

        tag_ids = self.env['standard.tags'].search(
            ['|', '|',
             ('id', '=', self.tag_id.id),
             ('parent_id', '=', self.tag_id.id),
             ('parent_id.parent_id', '=', self.tag_id.id)])

        #for i in tag_ids:
        #    _logger.info(i.name)

        consumidos = self.env['standard.request.line'].search([
            ('request_id.tag_id', 'in', tag_ids.ids),
            #('state', 'in', tag_ids.ids)
        ])

        data = {}
        for i in consumidos:
            data.setdefault(i.product_id, {'cant':0, 'pedido':0, 'comprado':0})

            data[i.product_id]['cant'] += i.qty
            data[i.product_id]['pedido'] += i.qty_done

        comprados = self.env['standard.distribution'].search([
            ('requisition_id.tag_ids.tag_id', 'in', tag_ids.ids)
        ])#.filtered(lambda r: r.requisition_id.purchase_ids)


        for i in comprados.filtered(lambda r: r.tag_id.id in tag_ids.ids):

            tags = []
            data.setdefault(i.product_id,
                            {'cant': 0, 'pedido': 0, 'comprado': 0})

            i.requisition_id.get_product_qty_receive()
                   
            data.setdefault(i.product_id, {'consumido': 0, 'comprado': 0})
            data[i.product_id]['comprado'] += i.product_qty_receive

        return data

    def print_report(self):
        return self.env.ref('standard_requests.report_standard').report_action(self)

