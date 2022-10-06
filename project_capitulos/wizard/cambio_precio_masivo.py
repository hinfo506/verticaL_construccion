from odoo import fields, models, api
from odoo.exceptions import ValidationError


class CambioPrecioMasivo(models.TransientModel):
    _name = "cambio.precio"

    nuevo_precio = fields.Float(string="Nuevo Coste", required=False)
    product_id = fields.Many2one(
        comodel_name="product.product", string="Artículo", required=True
    )
    project_id = fields.Many2one(
        comodel_name="project.project", string="Project_id", required=False
    )
    faseprincipal_id = fields.Many2one(
        comodel_name="fase.principal", string="Fase Principal", required=False
    )
    capitulo_id = fields.Many2one(
        comodel_name="capitulo.capitulo", string="Capitulo", required=False
    )
    subcapitulo_id = fields.Many2one(
        comodel_name="sub.capitulo", string="Subcapitulo", required=False
    )
    partida_id = fields.Many2one(
        comodel_name="partidas.partidas", string="Partida", required=False
    )
    is_guardado = fields.Boolean(string="Is_guardado", default=False)

    is_vacio = fields.Boolean(string="Is_vacio", default=False)

    item_ids = fields.Many2many(comodel_name="item.capitulo", string="Item")
    info = fields.Html(string="Info", required=False)
    mostrar_botones = fields.Boolean(string="Mostrar", default=True)

    # campos de Impuestos
    tipo_cambio = fields.Selection(
        string="Tipo cambio",
        selection=[
            ("nuevocoste", "Nuevo Coste"),
            ("todo", "Todo"),
            ("impuesto", "Nuevos Impuestos"),
        ],
        required=False,
    )

    tipo_descuento = fields.Selection(
        string="Tipo_descuento",
        selection=[
            ("cantidad", "cantidad"),
            ("porciento", "porciento"),
        ],
        required=False,
    )
    cant_descuento = fields.Float(string="Cant_descuento", required=False)
    beneficio_estimado = fields.Float(string="Beneficio Estimado en %", required=False)
    impuesto_porciento = fields.Float(string="Impuesto en % (ITBIS)", required=False)

    def vacio(self):
        # self.is_vacio=True
        if len(self.item_ids) == 0:
            self.is_vacio = False
        else:
            self.is_vacio = True

    # @api.depends('is_vacio')
    # def compute_direccion(self):
    #     # raise ValidationError(self.partida_id.name)
    #     self.info = str(self.project_id.name) + " " + str(self.project_id.capitulos_id.name)

    ######################################################
    ## aki tengo los item que pertenecen a ese proyecto ##
    ######################################################
    @api.onchange("product_id")
    def onchange_product(self):
        # hola = self.vacio()
        for record in self:
            if (
                (record.product_id and record.project_id)
                or record.capitulo_id
                or record.subcapitulo_id
                or record.partida_id
                or record.faseprincipal_id
            ):
                data = [
                    ("project_id", "=", record.project_id.id),
                    ("product_id", "=", record.product_id.id),
                ]
                if record.faseprincipal_id:
                    data = [
                        ("faseprincipal_id", "=", record.faseprincipal_id.id),
                        ("product_id", "=", record.product_id.id),
                    ]
                if record.capitulo_id:
                    data = [
                        ("capitulo_id", "=", record.capitulo_id.id),
                        ("product_id", "=", record.product_id.id),
                    ]
                if record.subcapitulo_id:
                    data = [
                        ("subcapitulo_id", "=", record.subcapitulo_id.id),
                        ("product_id", "=", record.product_id.id),
                    ]
                if record.partida_id:
                    data = [
                        ("partidas_id", "=", record.partida_id.id),
                        ("product_id", "=", record.product_id.id),
                    ]
                items = self.env["item.capitulo"].search(data)
                record.item_ids = items
                if len(items) == 0:
                    self.mostrar_botones = True
                if len(items) > 0:
                    self.mostrar_botones = False
                    self.vacio()

    def action_guardar_nuevo(self):
        # if self.product_id and self.nuevo_precio:
        if self.tipo_cambio == "nuevocoste":
            items = self.env["item.capitulo"].browse(self.item_ids.ids)
            items.write({"cost_price": self.nuevo_precio})
        elif self.tipo_cambio == "todo":
            items = self.env["item.capitulo"].browse(self.item_ids.ids)
            items.write(
                {
                    "cost_price": self.nuevo_precio,
                    "tipo_descuento": self.tipo_descuento,
                    "cantidad_descuento": self.cant_descuento,
                    "beneficio_estimado": self.beneficio_estimado,
                    "impuesto_porciento": self.impuesto_porciento,
                }
            )
        elif self.tipo_cambio == "impuesto":
            items = self.env["item.capitulo"].browse(self.item_ids.ids)
            items.write(
                {
                    "tipo_descuento": self.tipo_descuento,
                    "cantidad_descuento": self.cant_descuento,
                    "beneficio_estimado": self.beneficio_estimado,
                    "impuesto_porciento": self.impuesto_porciento,
                }
            )
        else:
            raise ValidationError("Debe seleccionar un Tipo de Cambio")

        return {
            "name": "Cambio Precio Masivo",
            "res_model": "cambio.precio",
            "view_mode": "form",
            "context": {
                "default_capitulo_id": self.capitulo_id.id
                if self.capitulo_id
                else False,
                # 'default_capitulo_id': self.faseprincipal_id.id if self.faseprincipal_id else False,
                "default_subcapitulo_id": self.subcapitulo_id.id
                if self.subcapitulo_id
                else False,
                "default_partida_id": self.partida_id.id if self.partida_id else False,
                "default_project_id": self.project_id.id,
                "default_is_guardado": True,
                # 'default_is_vacio': True,
            },
            "target": "new",
            "type": "ir.actions.act_window",
        }

    def action_guardar(self):
        if self.tipo_cambio == "nuevocoste":
            items = self.env["item.capitulo"].browse(self.item_ids.ids)
            items.write({"cost_price": self.nuevo_precio})
        elif self.tipo_cambio == "todo":
            items = self.env["item.capitulo"].browse(self.item_ids.ids)
            items.write(
                {
                    "cost_price": self.nuevo_precio,
                    "tipo_descuento": self.tipo_descuento,
                    "cantidad_descuento": self.cant_descuento,
                    "beneficio_estimado": self.beneficio_estimado,
                    "impuesto_porciento": self.impuesto_porciento,
                }
            )
        elif self.tipo_cambio == "impuesto":
            items = self.env["item.capitulo"].browse(self.item_ids.ids)
            items.write(
                {
                    "tipo_descuento": self.tipo_descuento,
                    "cantidad_descuento": self.cant_descuento,
                    "beneficio_estimado": self.beneficio_estimado,
                    "impuesto_porciento": self.impuesto_porciento,
                }
            )
        else:
            raise ValidationError("Debe seleccionar un Tipo de Cambio")
