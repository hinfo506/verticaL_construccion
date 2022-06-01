from odoo import fields, models, api


class Subcapitulo(models.Model):
    _inherit = 'sub.capitulo'

    def wizard_standar_partida(self):
        return {
            'name': 'Incluir Standar en Partida como Subcapitulo',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'add.standar',
            # 'context': {
            #     # 'default_is_vacio': True,
            #     # 'default_subcapitulo_id': self.id,
            #     # 'default_info': "LOS PRECIOS SERAN CAMBIADOS A PARTIR DE </br>" + "<strong>" + str(
            #     #     self.capitulo_id.project_id.name) + "/" + str(self.capitulo_id.name) + "/" + str(
            #     #     self.name) + " :</strong>",
            # },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

