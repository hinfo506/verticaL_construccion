from odoo import fields, models, api


class VerticalItem(models.Model):
    _name = "vertical.item"
    _inherit = "item.item"

    ##### DATOS PRINCIPALES  ########

    actual_quantity = fields.Float(
        string="Cantidad Comprada Actual",
    )
    hours = fields.Char(string="Horas", required=False)
    actual_timesheet = fields.Char(string="Parte de Horas Actual", required=False)
    base = fields.Char(string="Base", required=False)
    total_prevision = fields.Float("Importe Total Previsto")
    date = fields.Date(string="Fecha", default=lambda self: fields.Date.today())
    fecha_finalizacion = fields.Date("Fecha Finalización")
    condicion = fields.Selection(
        string="Condición",
        selection=[
            ("presupuestario", "Presupuestario"),
            ("sobrecoste", "Sobre Coste"),
            ("adicionales", "Adicionales"),
        ],
        required=False,
    )
    ###### FASES DEL PROYECTO ########
    project_id = fields.Many2one("project.project", string="Proyecto", ondelete="cascade")
    vertical_stage_id = fields.Many2one(comodel_name="vertical.stage", string="Fase", required=False)

    type_item = fields.Selection(string='Tipo de Item', selection=[
                    ('cost_analysis', 'Analisis de coste'),
                    ('standard', 'Standard'),
                    ('indefine', 'Indefinido'), ], required=False, default='indefine')

    ###### CAMPOS DESECHADOS ########
    longitud = fields.Float("Longitud", default=1)
    ancho = fields.Float("Ancho", default=1)
    alto = fields.Float("Alto", default=1)
    item_volumetry_ids = fields.One2many(
        comodel_name="vertical.item.volumetry",
        inverse_name="item_id",
        string="Item Volumetria",
        required=False,
    )
    # Campos Sumatorios
    item_volumetry_count = fields.Integer(
        string="item_volumetry_count",
        required=False,
        compute="_compute_item_volumetry_count",
    )
    color_item = fields.Selection(
        selection=[
            ("red", "Rojo"),
            ("blue", "Azul"),
            ("green", "Verde"),
            ("grey", "Gris"),
            ("brown", "Marrón"),
            ("purple", "Púrpura"),
        ],
        string="Color de la Linea",
        required=False,
    )

    estado_item = fields.Selection(
        string="Estado_partida",
        selection=[
            ("borrador", "Borrador"),
            ("aprobada", "Aprobada en Prevision"),
            ("aprobadaproceso", "Aprobada en Proceso"),
            ("pendiente", "Pdte Validar"),
            ("noaprobada", "No aprobada"),
        ],
        required=False,
        default="borrador",
    )

    cost_analysis_id = fields.Many2one(comodel_name='vertical.cost.analysis', string='Análisis de Coste', required=False)
    standard_id = fields.Many2one(comodel_name="standard", string="Standard", required=False)

    def _compute_item_volumetry_count(self):
        for r in self:
            r.item_volumetry_count = self.env["vertical.item.volumetry"].search_count([("item_id", "=", self.id)])

    def met_itemvolumetria(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Volumetria",
            "res_model": "vertical.item.volumetry",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.item_volumetry_ids.ids)],
            "context": dict(self._context, default_item_id=self.id),
        }

    @api.model
    def create(self, vals):
        record = super(VerticalItem, self).create(vals)
        if record.project_id and record.project_id.stage_id and record.project_id.stage_id.is_prevision:
            state = "aprobada" if record.project_id.stage_id.is_prevision else "pendiente"
            record.write({"estado_item": state})
        return record
