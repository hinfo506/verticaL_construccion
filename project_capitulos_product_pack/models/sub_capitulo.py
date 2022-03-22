# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models
from odoo.exceptions import UserError


class SubCapitulo(models.Model):
    _inherit = "sub.capitulo"


    # def write(self, vals):
    #     if "order_line" in vals:
    #         to_delete_ids = [e[1] for e in vals["order_line"] if e[0] == 2]
    #         subpacks_to_delete_ids = (
    #             self.env["sale.order.line"]
    #             .search(
    #                 [("id", "child_of", to_delete_ids), ("id", "not in", to_delete_ids)]
    #             )
    #             .ids
    #         )
    #         if subpacks_to_delete_ids:
    #             for cmd in vals["order_line"]:
    #                 if cmd[1] in subpacks_to_delete_ids:
    #                     if cmd[0] != 2:
    #                         cmd[0] = 2
    #                     subpacks_to_delete_ids.remove(cmd[1])
    #             for to_delete_id in subpacks_to_delete_ids:
    #                 vals["order_line"].append([2, to_delete_id, False])
    #     return super().write(vals)
