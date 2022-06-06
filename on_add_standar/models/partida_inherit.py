from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Partida(models.Model):
    _inherit = 'partidas.partidas'

    add_standar = fields.Boolean(string='Agregar Partida a traves de un Standar', required=False)
    standard_id = fields.Many2one(comodel_name='standard', string='Standard', required=False)
    line_ids = fields.Many2many(comodel_name='standard.line', string='Line_ids',store=True)

    @api.onchange('standard_id')
    def _onchange_FIELD_NAME(self):
        if self.standard_id:
            self.name = self.standard_id.name

    @api.onchange('add_standar')
    def _onchange_standar_id_vacio(self):
        if (self.add_standar == False) and self.standard_id:
            self.standard_id = 0

    #####################################
    ## Onchange para Agregar Las Fases ##
    #####################################
    @api.onchange('project_id')
    def _onchange_domain_project(self):
        fase = {}
        fase['domain'] = {'fase_principal_id': [('project_id', '=', self.project_id.id)]}
        return fase

    @api.onchange('fase_principal_id')
    def _onchange_domain_fase(self):
        cap = {}
        cap['domain'] = {'capitulo_id': [('fase_principal_id', '=', self.fase_principal_id.id)]}
        return cap

    @api.onchange('capitulo_id')
    def _onchange_domain_capitulo(self):
        sub = {}
        sub['domain'] = {'subcapitulo_id': [('capitulo_id', '=', self.capitulo_id.id)]}
        return sub
    ################################################################################################

    ####################################
    ## Cargar los item en modelo line ##
    ####################################
    @api.onchange('standard_id')
    def _onchange_cargar_line(self):
        for record in self:
            if record.standard_id:
                data = [('standard_id', '=', record.standard_id.id)]
                line = self.env['standard.line'].search(data)
                record.line_ids = line
    ####################################

    # def insertar_item(self,vals):
    #     if 'line_ids' in vals:
    #         for line in vals['line_ids']:
    #             items = vals.env['item.capitulo'].create({
    #                 'partidas_id': vals.id,
    #                 'subcapitulo_id': vals.subcapitulo_id.id,
    #                 'capitulo_id': vals.subcapitulo_id.capitulo_id.id,
    #                 'faseprincipal_id': vals.subcapitulo_id.fase_principal_id.id,
    #                 'project_id': vals.subcapitulo_id.project_id.id,
    #                 'cost_price': line.cost_price,
    #                 'product_id': line.product_id.id,
    #                 'uom_id': line.uom_id.id,
    #                 'product_qty': line.qty,
    #                 'descripcion': line.descripcion,
    #                 'job_type': line.job_type,
    #                 'subtotal_item_capitulo': line.subtotal_item_capitulo,
    #                 'tipo_descuento': line.tipo_descuento,
    #                 'cantidad_descuento': line.cantidad_descuento,
    #                 'subtotal_descuento': line.subtotal_descuento,
    #                 'beneficio_estimado': line.beneficio_estimado,
    #                 'importe_venta': line.importe_venta,
    #                 'impuesto_porciento': line.impuesto_porciento,
    #                 'total_impuesto_item': line.total_impuesto_item,
    #                 'suma_impuesto_item_y_cost_price': line.suma_impuesto_item_y_cost_price,
    #             })

    # @api.model
    # def create(self, vals):
    #
    #     # name = self.env['ir.sequence'].next_by_code('job.inspection.seq')
    #     vals.update({
    #         'estado_partida': 'pendiente',
    #     })
    #     record = super(Partida, self).create(vals)
    #     lines = self.env['standard.line'].search([('standard_id', '=', record.standard_id.id)])
    #     # raise ValidationError(lines)
    #     for line in lines:
    #         record.item_capitulo_ids = self.env['item.capitulo'].sudo().create({
    #             'partidas_id': record.id,
    #             'subcapitulo_id': record.subcapitulo_id.id,
    #             'capitulo_id': record.subcapitulo_id.capitulo_id.id,
    #             'faseprincipal_id': record.subcapitulo_id.fase_principal_id.id,
    #             'project_id': record.subcapitulo_id.project_id.id,
    #             'cost_price': 1,
    #             'product_id': line.product_id.id,
    #             'uom_id': line.uom_id.id,
    #             'product_qty': line.qty,
    #             'descripcion': line.descripcion,
    #             'job_type': 'material',
    #             'subtotal_item_capitulo': line.subtotal_item_capitulo,
    #             'tipo_descuento': line.tipo_descuento,
    #             'cantidad_descuento': line.cantidad_descuento,
    #             'subtotal_descuento': line.subtotal_descuento,
    #             'beneficio_estimado': line.beneficio_estimado,
    #             'importe_venta': line.importe_venta,
    #             'impuesto_porciento': line.impuesto_porciento,
    #             'total_impuesto_item': line.total_impuesto_item,
    #             'suma_impuesto_item_y_cost_price': line.suma_impuesto_item_y_cost_price,
    #         })

        # self.insertar_item(vals)
        # return super(Partida, self).create(vals)
        # self
        # self.estado_partida == 'pendiente'
    @api.model
    def create(self, vals):

        # name = self.env['ir.sequence'].next_by_code('job.inspection.seq')
        vals.update({
            'estado_partida': 'pendiente',
        })
        record = super(Partida, self).create(vals)
        lines = self.env['standard.line'].search([('standard_id', '=', record.standard_id.id)])
        # raise ValidationError(lines)
        for line in lines:
            record.item_capitulo_ids |= self.env['item.capitulo'].sudo().create({
                'partidas_id': record.id,
                'subcapitulo_id': record.subcapitulo_id.id,
                'capitulo_id': record.subcapitulo_id.capitulo_id.id,
                'faseprincipal_id': record.subcapitulo_id.fase_principal_id.id,
                'project_id': record.subcapitulo_id.project_id.id,
                'cost_price': 1,
                'product_id': line.product_id.id,
                    'uom_id': line.uom_id.id,
                    'product_qty': line.qty,
                    'descripcion': line.descripcion,
                    'job_type': 'material',
                    'subtotal_item_capitulo': line.subtotal_item_capitulo,
                    'tipo_descuento': line.tipo_descuento,
                    'cantidad_descuento': line.cantidad_descuento,
                    'subtotal_descuento': line.subtotal_descuento,
                    'beneficio_estimado': line.beneficio_estimado,
                    'importe_venta': line.importe_venta,
                    'impuesto_porciento': line.impuesto_porciento,
                    'total_impuesto_item': line.total_impuesto_item,
                    'suma_impuesto_item_y_cost_price': line.suma_impuesto_item_y_cost_price,
                })
        return record