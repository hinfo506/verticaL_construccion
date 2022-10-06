# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class SubCapitulo(models.Model):
    _inherit = "sub.capitulo"

    def write(self, vals):
        if "item_capitulo_materiales_ids" in vals:
            to_delete_ids = [
                e[1] for e in vals["item_capitulo_materiales_ids"] if e[0] == 2
            ]
            subpacks_to_delete_ids = (
                self.env["item.capitulo"]
                .search(
                    [("id", "child_of", to_delete_ids), ("id", "not in", to_delete_ids)]
                )
                .ids
            )
            if subpacks_to_delete_ids:
                for cmd in vals["item_capitulo_materiales_ids"]:
                    if cmd[1] in subpacks_to_delete_ids:
                        if cmd[0] != 2:
                            cmd[0] = 2
                        subpacks_to_delete_ids.remove(cmd[1])
                for to_delete_id in subpacks_to_delete_ids:
                    vals["item_capitulo_materiales_ids"].append(
                        [2, to_delete_id, False]
                    )
        return super().write(vals)
