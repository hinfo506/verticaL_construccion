import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ChangeProduct(models.TransientModel):
    _name = 'change.product'

    product_id = fields.Many2one(comodel_name='product.product', string='Artículo', required=True)
    nuevo_precio = fields.Float(string='Nuevo Coste', required=False)
    product_change_id = fields.Many2one(comodel_name='product.product', string='Sustituir Por', required=True)
    change_price = fields.Boolean(string='Cambiar Precio', required=False)

    info = fields.Html(string='Info', required=False)

    item_ids = fields.Many2many(comodel_name='item.capitulo', string='Item')

    # Fases
    project_id = fields.Many2one(comodel_name='project.project', string='Project_id', required=False)
    faseprincipal_id = fields.Many2one(comodel_name='fase.principal', string='Fase Principal', required=False)
    capitulo_id = fields.Many2one(comodel_name='capitulo.capitulo', string='Capitulo', required=False)
    subcapitulo_id = fields.Many2one(comodel_name='sub.capitulo', string='Subcapitulo', required=False)
    partida_id = fields.Many2one(comodel_name='partidas.partidas', string='Partida', required=False)

    ######################################################
    ## aki tengo los item que pertenecen a ese proyecto ##
    ######################################################
    @api.onchange('product_id')
    def onchange_product(self):
        # hola = self.vacio()
        for record in self:
            if (
                    record.product_id and record.project_id) or record.capitulo_id or record.subcapitulo_id or record.partida_id or record.faseprincipal_id:
                data = [('project_id', '=', record.project_id.id), ('product_id', '=', record.product_id.id)]
                if record.faseprincipal_id:
                    data = [('faseprincipal_id', '=', record.faseprincipal_id.id),
                            ('product_id', '=', record.product_id.id)]
                if record.capitulo_id:
                    data = [('capitulo_id', '=', record.capitulo_id.id), ('product_id', '=', record.product_id.id)]
                if record.subcapitulo_id:
                    data = [('subcapitulo_id', '=', record.subcapitulo_id.id),
                            ('product_id', '=', record.product_id.id)]
                if record.partida_id:
                    data = [('partidas_id', '=', record.partida_id.id), ('product_id', '=', record.product_id.id)]
                items = self.env['item.capitulo'].search(data)
                record.item_ids = items
                # if len(items) == 0:
                #     self.mostrar_botones = True
                # if len(items) > 0:
                #     self.mostrar_botones = False
                # hola = self.vacio()

    def action_guardar(self):
        if self.product_id == self.product_change_id:
            raise ValidationError('Los productos no pueden ser iguales')
        else:
            if self.item_ids:
                if self.product_id and self.product_change_id:
                    items = self.env['item.capitulo'].browse(self.item_ids.ids)
                    # raise ValidationError(items)
                    if self.change_price:
                        items.write({
                            'cost_price': self.nuevo_precio,
                            'product_id': self.product_change_id.id
                        })
                    else:
                        items.write({
                            'product_id': self.product_change_id.id
                        })
            else:
                raise ValidationError('No hay pruductos que coincidan')
