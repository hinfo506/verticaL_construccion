# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Catalogue(models.Model):
    _name = 'catalogue.catalogue'

    name = fields.Char(string='Nombre')
    codigo = fields.Char(string='Código', required=False)
    create_date = fields.Datetime(string='Creado en', required=False, readonly=True, default=lambda self: fields.Datetime.now())

    # Fases
    project_id = fields.Many2one(comodel_name='project.project', string='Project_id', required=False)
    fase_principal_id = fields.Many2one(comodel_name='fase.principal', string='Fase Principal', required=False)
    capitulo_id = fields.Many2one(comodel_name='capitulo.capitulo', string='Capitulo', required=False)
    subcapitulo_id = fields.Many2one(comodel_name='sub.capitulo', string='Subcapitulo', required=False)
    partida_id = fields.Many2one(comodel_name='partidas.partidas', string='Partida', required=False)

    line_purchase_ids = fields.One2many(comodel_name='line.purchase', inverse_name='catalogue_id', string='Line_purchase_ids', required=False)

    def generar_line_purchase(self):
        if self.project_id:
            product = self.env['item.capitulo'].search([('project_id', '=', self.project_id.id)]).mapped("product_id")
            for p in product:
                # raise ValidationError(p)
                purchase = self.line_purchase_ids.create({
                    'product_id': p.id,
                })
            # raise ValidationError(product)
        else:
            raise ValidationError('Debe seleccionar un Proyecto')