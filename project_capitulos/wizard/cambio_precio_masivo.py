from odbc import dataError
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class CambioPrecioMasivo(models.TransientModel):
    _name = 'cambio.precio'

    nuevo_precio = fields.Float(string='Nuevo Coste', required=False)
    product_id = fields.Many2one(comodel_name='product.product', string='Artículo', required=False)
    project_id = fields.Many2one(comodel_name='project.project', string='Project_id', required=False)
    capitulo_id = fields.Many2one(comodel_name='capitulo.capitulo', string='Capitulo', required=False)
    subcapitulo_id = fields.Many2one(comodel_name='sub.capitulo', string='Subcapitulo', required=False)
    partida_id = fields.Many2one(comodel_name='partidas.partidas', string='Partida', required=False)
    is_guardado = fields.Boolean(string='Is_guardado',default=False)
    item_ids = fields.Many2many(comodel_name='item.capitulo', string='Item')

    # aki tengo los item que pertenecen a ese proyecto
    @api.onchange('product_id')
    def onchange_product(self):
        for record in self:
            if (record.product_id and record.project_id) or record.capitulo_id or record.subcapitulo_id or record.partida_id:
                data = [('project_id', '=', record.project_id.id), ('product_id', '=', record.product_id.id)]
                if record.capitulo_id:
                    # data.append(('capitulo_id','=',record.capitulo_id))
                    data = [('capitulo_id', '=', record.capitulo_id.id), ('product_id', '=', record.product_id.id)]
                if record.subcapitulo_id:
                    data = [('subcapitulo_id', '=', record.subcapitulo_id.id), ('product_id', '=', record.product_id.id)]
                if record.partida_id:
                    data = [('partidas_id', '=', record.partida_id.id), ('product_id', '=', record.product_id.id)]
                items = self.env['item.capitulo'].search(data)
                record.item_ids = items


    def action_guardar_nuevo(self):
        items = self.env['item.capitulo'].browse(self.item_ids.ids)
        items.write({'cost_price': self.nuevo_precio})
        return {
            'name': 'Cambio Precio Masivo',
            'res_model': 'cambio.precio',
            'view_mode': 'form',
            'context': {
                'default_capitulo_id': self.capitulo_id.id if self.capitulo_id else False,
                'default_subcapitulo_id': self.subcapitulo_id.id if self.subcapitulo_id else False,
                'default_partida_id': self.partida_id.id if self.partida_id else False,
                'default_project_id': self.project_id.id,
                'default_is_guardado': True,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    def action_guardar(self):
        items = self.env['item.capitulo'].browse(self.item_ids.ids)
        items.write({'cost_price': self.nuevo_precio})
