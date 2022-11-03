# -*- coding: utf-8 -*-
from odoo import fields, models


class VerticalBills(models.Model):
    _name = "vertical.bills"

    type_cost = fields.Selection(
        string="Type_cost",
        selection=[
            ("nomina", "Nómina"),
            ("aduana", "Aduana"),
            ("transporteterrestre", "Transporte Terrestre"),
            ("gastosvarios", "Gastos Varios"),
        ],
        required=False,
    )

    description = fields.Text(string="Descripción", required=False)
    amount_cost = fields.Float(string="Importe del Coste", required=False)
    tax_cost = fields.Float(string="Impuesto del Coste", required=False)

    stage_id = fields.Many2one(
        comodel_name="vertical.stage", string="Stage_id", required=False
    )
