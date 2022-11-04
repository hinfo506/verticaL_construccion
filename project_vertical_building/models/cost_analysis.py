from odoo import fields, models
from odoo.exceptions import ValidationError


class VerticalCostAnalysis(models.Model):
    _name = "vertical.cost.analysis"

    name = fields.Char("Nombre")
    code = fields.Char(string="Código", required=False)
    standard_id = fields.Many2one(comodel_name="standard", string="Standard")
    cost_analysis_line_ids = fields.One2many(
        comodel_name="cost.analysis.line",
        inverse_name="cost_analysis_id",
        string="Cost_analysis_line_ids",
        required=False,
    )
    cost_standard = fields.Float(
        string="", required=False, related="standard_id.total_cost"
    )
    cost_cost_analysis = fields.Float(
        string="Total Coste", required=False, compute="_compute_amount_cost_total"
    )

    item_ids = fields.One2many(
        comodel_name="vertical.item",
        inverse_name="cost_analysis_id",
        string="Item_ids",
        required=False,
    )

    def _compute_amount_cost_total(self):
        for record in self:
            sumatoria = 0
            if record.cost_standard or record.cost_analysis_line_ids:
                sumatoria = record.cost_standard + sum(
                    c.suma_impuesto_item_y_cost_price
                    for c in record.cost_analysis_line_ids
                )
            record.cost_cost_analysis = sumatoria

    def action_throw_changes(self):
        # fases = self.env['vertical.stage'].search([('cost_analysis_id', '=', self.id)]).mapped('order_id')
        fases = self.env["vertical.stage"].search([("cost_analysis_id", "=", self.id)])
        raise ValidationError(fases)
