# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class StandardLine(models.Model):
    _name = 'standard.line'
    _description = 'Standard Line'

    standard_id = fields.Many2one('standard', string='Estandar')
    product_id = fields.Many2one('product.product', string='Producto', required=1)
    uom_id = fields.Many2one('uom.uom', string='Unidad de Medida', required=1)
    qty = fields.Float(string='Cantidad', required=1)
    descripcion = fields.Char(string='Descripción')

    # Agregados para matchear con item
    job_type = fields.Selection(
        selection=[('material', 'Materiales'),
                   ('labour', 'Mano de Obra'),
                   ('overhead', 'Gastos Generales'),
                   ('machinery', 'Maquinaria')],
        string="Tipo de Costo",
        required=False, )
    cost_price = fields.Float(string='Precio Coste', copy=False, )
    subtotal_item_capitulo = fields.Float(string='Subtotal', store=False, compute='_compute_subtotal_item_capitulo')
    tipo_descuento = fields.Selection(string='Tipo descuento Proveedor',
                                      selection=[('cantidad', 'cantidad'), ('porciento', 'porciento'), ],
                                      required=False, )
    cantidad_descuento = fields.Float(string='Cantidad Descuento', required=False)
    subtotal_descuento = fields.Float(string='Subtotal Con descuento', required=False,
                                      compute='_compute_subtotal_descuento', store=False)
    beneficio_estimado = fields.Float(string='Beneficio Estimado en %', required=False)
    importe_venta = fields.Float(string='Importe Venta (PVP)', required=False, compute='_compute_subtotal_descuento',
                                 store=False)
    impuesto_porciento = fields.Float(string='Impuesto en % (ITBIS)', required=False)
    total_impuesto_item = fields.Float(string='Importe ITBIS', required=False, compute='_compute_subtotal_descuento',
                                       store=False)
    suma_impuesto_item_y_cost_price = fields.Float(string='Total (P.U. + ITBIS)', required=False,
                                                   compute='_compute_subtotal_descuento', store=False)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        domain = {}

        if not self.product_id:
            domain['uom_id'] = []

        if not self.uom_id or self.product_id.uom_id.category_id.id \
                != self.uom_id.category_id.id:
            self.uom_id = self.product_id.uom_id.id

        domain['uom_id'] = [('category_id', '=', self.product_id.uom_id.category_id.id)]

        return {'domain': domain}