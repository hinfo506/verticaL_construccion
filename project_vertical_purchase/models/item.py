from odoo import fields, models, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class VerticalItem(models.Model):
    _inherit = 'vertical.item'
    
    amount_confirm = fields.Float(string='Amount_confirm', required=False)
    amount_delivered = fields.Float(string='Amount_delivered', required=False)

    # def purchase_from_item(self):
    #     act_ids = self.env.context.get('active_ids')
    #     item_ids = self.env['vertical.item'].search([('id', '=', act_ids)])
    #     # raise ValidationError(item_ids[0].vertical_stage_id)
    #     #
    #     # for i in item_ids:
    #     #     if i.stage_id != item_ids[0].stage_id:
    #     #         pass
    #
    #     purchase = self.env['purchase.order'].create({
    #         'partner_id': self.env.user.id,
    #         'stage_id': item_ids[0].vertical_stage_id.id,
    #     })
    #     for i in item_ids:
    #         # for i in item.item_ids:
    #         purchase_line = self.env['purchase.order.line'].create({
    #             'order_id': purchase.id,
    #             'product_id': i.product_id.id,
    #             'name': 'esta es la descripcion',
    #             'product_qty': i.product_qty,
    #             'price_unit': i.cost_price,
    #             'item_id': i.id,
    #         })


    def purchase_from_item(self):
        po_obj = 'purchase.order'
        act_ids = self.env.context.get('active_ids',[])
        items = self.browse(act_ids)
        product_ids = items.mapped('product_id')
        # Recupero los proveedores relacionados
        vendors = self.env['product.supplierinfo'].search([
            '|',
            ('product_id', 'in', product_ids.mapped('id')),
            ('product_tmpl_id','in', product_ids.mapped('product_tmpl_id'))
        ])
        # Por cada proveedor, debo revisar si tengo al menos una PO en borrador y las guardo en un diccionario
        purchase_data = {}
        purchase_orders = {}
        purchase_order_lines = {}
        for vendor in vendors:
            po = po_obj.search([('partner_id', '=', vendor.name.id)], limit=1)
            p_data = {}
            if len(po) == 1:
                # Voy a meter las purchase_order_lines que genere en las purchase_orders, tengo esto en 2 diccionarios
                p_data['purchase_order'] = po[0].id
            p_data['order_lines'] = []
            purchase_data[vendor.name.id] = p_data
        # por cada producto, debo verificar las cantidades minimas del vendor y proceder
        for item in items:
            # Me interesan solo los que esten activos
            for seller in item.product.seller_ids.filtered(lambda s: s.name.active):
                # revisar en la configuración del seller las cantidades y comparar que sea mayor o igual
                if seller.min_qty <= item.product_qty:
                    product_lang = item.product_id.with_prefetch().with_context(
                        lang=seller.name.lang,
                        partner_id=seller.name.id,
                    )
                    name = product_lang.with_context(seller_id=seller.id).display_name
                    if product_lang.description_purchase:
                        name += '\n' + product_lang.description_purchase
                    po_line_vals = {
                        'name': name,
                        'product_qty': item.product_qty,
                        'product_id': item.product_id.id,
                        'product_uom': product_id.uom_po_id.id,
                        'price_unit': price_unit,
                        'date_planned': date_planned,
                        'taxes_id': [(6, 0, taxes.ids)],
                        'order_id': po.id,
                    }
                    new_po_line = self.env['purchase.order.line'].create(po_line_vals)
                    purchase_data[seller.name.id]['order_lines'].append(new_po_line.id)

        # Voy a ciclar por las lineas creadas, que estan agrupadas en el diccionario
        for po_lines_key in purchase_order_lines.keys():
            # Ya existe una purchase order, no debo crearla
            current_po = False
            must_update_dict = False
            if po_lines_key in purchase_orders:
                # Busco en la DB
                current_po = po_obj.browse(purchase_orders[po_lines_key])
                must_update_dict = True
            else:
                #debo crear una nueva PO para el proveedor seleccionado
                current_po = po_obj.create({
                    'partner_id': po_lines_key, # mi identificador del diccionario es el id del proveedor, lo obtuve arriba
                    'stage_id': item_ids[0].vertical_stage_id.id,
                })
            for pol_id in purchase_order_lines[po_lines_key]:
                # Agrego cada linea creada a la PO correspondiente.
                current_po.order_line = [(4, pol_id)]
            if must_update_dict:
                purchase_orders[po_lines_key] = current_po.id
        




        
        # purchase_order.order_line = [(4, new_po_line.id)]

        # item_ids = self.env['vertical.item'].search([('id', 'in', act_ids)])

        # raise ValidationError(item_ids[0].vertical_stage_id)
        #
        # for i in item_ids:
        #     if i.stage_id != item_ids[0].stage_id:
        #         pass

        # purchase = self.env['purchase.order'].create({
        #     'partner_id': self.env.user.id,
        #     'stage_id': item_ids[0].vertical_stage_id.id,
        # })
        # product.template

        data = []
        for i in item_ids:
            data += i.product_id.seller_ids.name

        raise ValidationError(data)
