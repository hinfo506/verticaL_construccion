import logging
from odoo import fields, models
_logger = logging.getLogger(__name__)


class Standard(models.Model):
    _name = "standard"
    _description = "Standard"
    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char(string="Nombre", required=1)
    code = fields.Char(string="Código", required=False)
    parent_id = fields.Many2one("standard", string="Padre")
    # line_ids = fields.One2many('standard.line', 'standard_id', copy=True)
    line_ids = fields.One2many(
        comodel_name="standard.line",
        inverse_name="standard_id",
        string="Line_ids",
        copy=True,
    )
    parent_path = fields.Char()
    ref_proyecto = fields.Char("Proyecto")
    ref_etapa = fields.Char("Etapa")
    is_purchase = fields.Boolean(string="Aparece en Req. Compras")
    is_warehouse = fields.Boolean(string="Aparece en Req. Almacen")

    total_cost = fields.Float(
        string="Total coste", required=False, compute="_compute_total_cost"
    )

    def _compute_total_cost(self):
        for rec in self:
            total = 0
            if rec.line_ids:
                total = sum(rec.line_ids.mapped("suma_impuesto_item_y_cost_price"))
            rec.update({"total_cost": total})
