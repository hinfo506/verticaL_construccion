from odoo import fields, models, api


class FaseInicial(models.Model):
    _name = 'fase.inicial'

    name = fields.Char()

    # FASES DEL PROYECTO
    capitulos_id = fields.One2many(comodel_name='capitulo.capitulo', inverse_name='fase_inicial_id', string='Capitulos_id', required=False)
    # item_ids = fields.One2many(comodel_name='item.capitulo', inverse_name='project_id', string='Item_ids', required=False)
