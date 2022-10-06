from odoo import models


class Subcapitulo(models.Model):
    _inherit = "sub.capitulo"

    def on_change_product(self):
        return {
            "name": "Cambiar Producto",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "change.product",
            "context": {
                "default_subcapitulo_id": self.id,
                "default_info": "LOS PRODUCTOS SERAN CAMBIADOS A PARTIR DE : </br>"
                + "<strong>"
                + str(self.capitulo_id.project_id.name)
                + "/"
                + str(self.fase_principal_id.name)
                + "/"
                + str(self.capitulo_id.name)
                + "/"
                + str(self.name)
                + " :</strong>",
            },
            "type": "ir.actions.act_window",
            "target": "new",
        }
