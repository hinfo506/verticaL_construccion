# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class VerticalStage(models.Model):
    _inherit = "vertical.stage"

    purchase_count = fields.Integer(
        string="purchase_count", required=False, compute="_compute_purchase_count"
    )

    # @api.depends('item_ids')
    def _compute_purchase_count(self):
        for r in self:
            r.purchase_count = self.env["purchase.order"].search_count(
                [("stage_id", "=", r.id)]
            )  # Esta consulta es menos eficiente que simplemente contar los item_ids
            # r.purchase_count = len(r.item_ids)

    def action_view_purchase(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Compras",
            "res_model": "purchase.order",
            "view_mode": "tree,form",
            "domain": [("stage_id", "=", self.id)],
            "context": {
                "create": False,
            },
        }

    def confirmed_suppliers(self):
        act_ids = self.env.context.get("active_ids", [])  # tomar ids activos
        stages = self.browse(
            act_ids
        )  # tomar el modelo y los ids que seleccione vertical.stage(89, 90)
        items = stages.mapped(
            "item_ids"
        )  # tomo las fases y mapeo por los item obteniendo el modelo vertical.item(5, 6, 7)
        for i in items:
            if not i.product_id.seller_ids:
                raise ValidationError(_("No se pudo completar la venta: Hay Artículos sin proveedores"))

    @api.model
    def purchase_from_stage(self):
        self.confirmed_suppliers()

        company_id = self.env.user.company_id
        po_obj = self.env["purchase.order"]
        act_ids = self.env.context.get("active_ids", [])
        stages = self.browse(act_ids)
        itemss = stages.mapped("item_ids")
        items = self.env["vertical.item"].search(
            [("job_type", "=", "material"), ("id", "in", itemss.ids)]
        )
        product_ids = items.mapped("product_id")
        # Recupero los proveedores relacionados
        vendors = self.env["product.supplierinfo"].search(
            [
                "|",
                ("product_id", "in", product_ids.mapped("id")),
                ("product_tmpl_id", "in", product_ids.mapped("product_tmpl_id.id")),
            ]
        )
        # Por cada proveedor, debo revisar si tengo al menos una PO en borrador y las guardo en un diccionario
        purchase_data = {}
        for vendor in vendors:
            po = po_obj.search([("partner_id", "=", vendor.name.id)], limit=1)
            p_data = {}
            if len(po) == 1:
                # Voy a meter las purchase_order_lines que genere en las purchase_orders, tengo esto en 2 diccionarios
                p_data["purchase_order"] = po[0].id
            p_data["order_lines"] = []
            purchase_data[vendor.name.id] = p_data
        _logger.info("purchase_data: ")
        _logger.info(purchase_data)
        # por cada producto, debo verificar las cantidades minimas del vendor y proceder
        for item in items:
            # if item.job_type == 'material':
            # Me interesan solo los que esten activos
            for seller in item.product_id.seller_ids.filtered(lambda s: s.name.active):
                # revisar en la configuración del seller las cantidades y comparar que sea mayor o igual
                if seller.min_qty <= item.product_qty:
                    taxes = item.product_id.supplier_taxes_id.filtered(
                        lambda x: x.company_id.id == company_id.id
                    )
                    product_lang = item.product_id.with_prefetch().with_context(
                        lang=seller.name.lang,
                        partner_id=seller.name.id,
                    )
                    name = product_lang.with_context(seller_id=seller.id).display_name
                    if product_lang.description_purchase:
                        name += "\n" + product_lang.description_purchase
                    po_line_vals = {
                        "name": name,
                        "product_qty": item.product_qty,
                        "product_id": item.product_id.id,
                        "product_uom": item.product_id.uom_po_id.id,
                        "price_unit": item.cost_price,
                        "taxes_id": [(6, 0, taxes.ids)],
                        "item_id": item.id,
                    }
                    purchase_data[seller.name.id]["order_lines"].append(
                        (0, False, po_line_vals)
                    )

        # Voy a ciclar por las lineas creadas, que estan agrupadas en el diccionario
        purchase_orders = []
        _logger.info("purchase_data.keys(): ")
        _logger.info(purchase_data.keys())
        for vendor_key in purchase_data.keys():
            # Ya existe una purchase order, no debo crearla
            current_po = False
            if "purchase_order" in purchase_data[vendor_key]:
                # Busco en la DB
                current_po = po_obj.browse(purchase_data[vendor_key]["purchase_order"])
            else:
                # debo crear una nueva PO para el proveedor seleccionado
                current_po = po_obj.create(
                    {
                        "partner_id": vendor_key,
                        # mi identificador del diccionario es el id del proveedor, lo obtuve arriba
                        "stage_id": item[0].vertical_stage_id.id,
                    }
                )
                purchase_data[vendor_key]["purchase_order"] = current_po.id
                # Actualizo mi dict

            current_po.order_line = purchase_data[vendor_key]["order_lines"]
            purchase_orders.append(current_po.id)

