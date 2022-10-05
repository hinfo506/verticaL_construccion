from odoo import models


class Subcapitulo(models.Model):
    _inherit = 'sub.capitulo'

    def wizard_standar_partida(self):
        return {
            'name': 'Incluir Standar en Partida desde Subcapitulo',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'add.standar',
            'context': {
                #     # 'default_is_vacio': True,
                'default_subcapitulo_id': self.id,
                'default_info': "El STANDAR SE INCLUIRÁ COMO UNA NUEVA PARTIDA EN EL SUBCAPITULO: </br>" + "<strong>" + str(
                    self.capitulo_id.project_id.name) + "/" + str(self.fase_principal_id.name) + "/" + str(
                    self.capitulo_id.name) + "/" + str(
                    self.name) + " :</strong>",
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

        # return {
        #     'name': 'Incluir Standar en Partida como Subcapitulo',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'standard.request',
        #     # 'context': {
        #     #     # 'default_is_vacio': True,
        #     #     # 'default_subcapitulo_id': self.id,
        #     #     # 'default_info': "LOS PRECIOS SERAN CAMBIADOS A PARTIR DE </br>" + "<strong>" + str(
        #     #     #     self.capitulo_id.project_id.name) + "/" + str(self.capitulo_id.name) + "/" + str(
        #     #     #     self.name) + " :</strong>",
        #     # },
        #     'type': 'ir.actions.act_window',
        #     'target': 'new',
        # }
