from odoo import api, fields, models


class ItemItem(models.Model):
    _name = "item.item"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "product_id"

    descripcion = fields.Text("Descripción")
    product_id = fields.Many2one("product.product", string="Producto", required=1)
    product_qty = fields.Float(
        string="Cantidad Planificada", copy=False, digits=(12, 2), required=1
    )
    uom_id = fields.Many2one(
        "uom.uom", string="Unid. de Medida",
    )
    reference = fields.Char(string="Referencia", copy=False)
    job_type = fields.Selection(
        selection=[
            ("material", "Materiales"),
            ("labour", "Mano de Obra"),
            ("overhead", "Gastos Generales"),
            ("machinery", "Maquinaria"),
        ],
        string="Tipo de Costo",
        required=True
    )

    subtotal_item_capitulo = fields.Float(
        string="Subtotal", store=False, compute="_compute_subtotal_item_capitulo"
    )
    tipo_descuento = fields.Selection(
        string='Tipo Dto.',
        selection=[
            ('cantidad', 'cantidad'),
            ('porciento', 'porciento'),
        ],
        required=False,
    )
    cantidad_descuento = fields.Float(string='Imp. Dto.', required=False)
    subtotal_descuento = fields.Float(
        string='Subtotal Con descuento',
        required=False,
        compute='_compute_subtotal_descuento',
        store=False
    )
    beneficio_estimado = fields.Float(string='% Benef.', required=False)
    importe_venta = fields.Float(
        string='Importe Venta (PVP)',
        required=False,
        compute='_compute_subtotal_descuento',
        store=False
    )
    impuesto_porciento = fields.Float(string='ITBIS %', required=False)
    total_impuesto_item = fields.Float(
        string='Importe ITBIS',
        required=False,
        compute='_compute_subtotal_descuento',
        store=False
    )
    suma_impuesto_item_y_cost_price = fields.Float(
        string='Total (P.U. + ITBIS)',
        required=False,
        compute='_compute_subtotal_descuento',
        store=False
    )
    cost_price = fields.Float(
        string='Coste',
        copy=False,
    )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        for rec in self:
            rec.descripcion = rec.product_id.name
            rec.product_qty = 1.0
            rec.uom_id = rec.product_id.uom_id.id
            rec.cost_price = rec.product_id.standard_price  # lst_price

    # Importe Subtotal item Capitulo - Importe sin contar con los impuestos
    @api.depends("product_qty", "cost_price")
    def _compute_subtotal_item_capitulo(self):
        for rec in self:
            if rec.job_type in ["material", "labour"]:
                rec.subtotal_item_capitulo = rec.product_qty * rec.cost_price
            elif rec.job_type == "machinery":
                rec.subtotal_item_capitulo = (
                    rec.product_qty * 3
                )  # AQUI TIENE QUE IR, EN VEZ DE EL 3 EL TOTAL DE MATERIAL + LABOUR Y QUE PRODUCT_QTY SEA UN %
            else:
                rec.subtotal_item_capitulo = 0

    # Importe Subtotal item Capitulo - Importe sin contar con los impuestos
    @api.depends("product_qty", "cost_price")
    def _compute_subtotal(self):
        for rec in self:
            if rec.job_type == "material":
                rec.subtotal_item_capitulo = rec.product_qty * rec.cost_price
            elif rec.job_type == "labour":
                rec.subtotal_item_capitulo = rec.product_qty * rec.cost_price
            elif rec.job_type == "machinery":
                rec.subtotal_item_capitulo = (
                        rec.product_qty * 3
                )  # AQUI TIENE QUE IR, EN VEZ DE EL 3 EL TOTAL DE MATERIAL + LABOUR Y QUE PRODUCT_QTY SEA UN %
            else:
                rec.subtotal_item_capitulo = 0

    # Importe Subtotal item Capitulo - Importe con los impuestos
    @api.depends(
        'tipo_descuento',
        'product_qty',
        'cost_price',
        'subtotal_item_capitulo',
        'cantidad_descuento',
        'beneficio_estimado',
        'impuesto_porciento'
    )
    def _compute_subtotal_descuento(self):
        for record in self:
            if record.tipo_descuento == "cantidad":
                record.subtotal_descuento = (
                        record.subtotal_item_capitulo - record.cantidad_descuento
                )
            elif record.tipo_descuento == "porciento":
                record.subtotal_descuento = record.subtotal_item_capitulo - (
                        (record.subtotal_item_capitulo * record.cantidad_descuento) / 100
                )
            else:
                record.subtotal_descuento = record.subtotal_item_capitulo

            record.importe_venta = (
                (record.subtotal_item_capitulo * record.beneficio_estimado) / 100
            ) + record.subtotal_item_capitulo
            record.total_impuesto_item = record.subtotal_descuento * (
                record.impuesto_porciento / 100
            )
            record.suma_impuesto_item_y_cost_price = (
                record.subtotal_descuento + record.total_impuesto_item
            )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        domain = {}
        if not self.product_id:
            domain["uom_id"] = []
        if (
            not self.uom_id
            or self.product_id.uom_id.category_id.id != self.uom_id.category_id.id
        ):
            self.uom_id = self.product_id.uom_id.id
        domain["uom_id"] = [("category_id", "=", self.product_id.uom_id.category_id.id)]
        return {"domain": domain}

    def action_standar_line(self):
        return {
            'type': "ir.actions.act_window",
            'res_model': self._name,
            'res_id': self.id,
            'view_type': "form",
            'view_mode': "form",
            'target': "new",
        }

    # Onchage para cambiar el dominio
    @api.onchange("job_type")
    def _onchange_domain_product(self):
        product = {}
        if self.job_type == "labour":
            product["domain"] = {"product_id": [("detailed_type", "=", "service")]}
            return product
        else:
            product["domain"] = {"product_id": [("detailed_type", "!=", "service")]}
            return product
