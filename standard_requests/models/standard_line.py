# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class StandardLine(models.Model):
    _name = 'standard.line'
    _description = 'Standard Line'

    standard_id = fields.Many2one('standard', string='Estandar')
    product_id = fields.Many2one('product.product', string='Producto', required=1)
    uom_id = fields.Many2one('uom.uom', string='Unidad de Medida', required=1)
    qty = fields.Float(string='Cantidad', required=1)
    descripcion = fields.Text(string="Descripción", required=False)

    # Agregados para matchear con item
    job_type = fields.Selection(
        selection=[('material', 'Materiales'),
                   ('labour', 'Mano de Obra'),
                   ('overhead', 'Gastos Generales'),
                   ('machinery', 'Maquinaria')],
        string="Tipo de Costo",
        required=True, )
    cost_price = fields.Float(string='Precio Coste', copy=False, )
    subtotal_item_capitulo = fields.Float(string='Subtotal', store=False, compute='_compute_subtotal')
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

    # Importe Subtotal item Capitulo - Importe sin contar con los impuestos
    @api.depends('qty', 'cost_price')
    def _compute_subtotal(self):
        # raise ValidationError('sda')
        for rec in self:
            if rec.job_type == 'material':
                rec.subtotal_item_capitulo = rec.qty * rec.cost_price
            elif rec.job_type == 'labour':
                rec.subtotal_item_capitulo = rec.qty * rec.cost_price
            elif rec.job_type == 'machinery':
                rec.subtotal_item_capitulo = rec.qty * 3  # AQUI TIENE QUE IR, EN VEZ DE EL 3 EL TOTAL DE MATERIAL + LABOUR Y QUE PRODUCT_QTY SEA UN %
            else:
                rec.subtotal_item_capitulo = 0

    # Importe Subtotal item Capitulo - Importe con los impuestos
    @api.depends('tipo_descuento','qty', 'cost_price', 'subtotal_item_capitulo', 'cantidad_descuento','beneficio_estimado','impuesto_porciento')
    def _compute_subtotal_descuento(self):
        for record in self:
            if record.tipo_descuento == 'cantidad':
                record.subtotal_descuento = record.subtotal_item_capitulo - record.cantidad_descuento
            elif record.tipo_descuento == 'porciento':
                record.subtotal_descuento = record.subtotal_item_capitulo - ((record.subtotal_item_capitulo*record.cantidad_descuento)/100)
            else:
                record.subtotal_descuento = record.subtotal_item_capitulo

            record.importe_venta = ((record.subtotal_item_capitulo * record.beneficio_estimado) / 100) + record.subtotal_item_capitulo
            record.total_impuesto_item = record.subtotal_descuento * (record.impuesto_porciento / 100)
            record.suma_impuesto_item_y_cost_price = record.subtotal_descuento + record.total_impuesto_item

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

    @api.onchange('product_id')
    def _onchan_product_id(self):
        for rec in self:
            rec.descripcion = rec.product_id.name
            rec.qty = 1.0
            rec.uom_id = rec.product_id.uom_id.id
            rec.cost_price = rec.product_id.standard_price  # lst_price

    # Revisar este metodo aqui debe llevarme al item
    def action_standar_line(self):
        # raise ValidationError('menos mal')
        return {
            'name': 'Item',
            # 'name': self.cliente_id.name,
            'view_type': 'form',
            'view_mode': 'form',
            # 'res_id': self.id,
            'res_model': 'item.capitulo',
            # 'context': {
            #     'default_cliente_id': self.cliente_id.id,
            #     'default_sol_p_id': self.id,
            #     'default_area_ids': self._context.get('area_ids', [])
            # },
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('project_capitulos.itemsubcapitulo_view_form').id, 'form')],
            'target': 'new',
        }

        # return {
        #     'res_id': self.id,
        #     'res_model': 'item.capitulo',
        #     'target': 'new',
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        # }