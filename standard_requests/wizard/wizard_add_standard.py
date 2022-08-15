from odoo import fields, models, api
from odoo.exceptions import ValidationError

class AddStandar(models.TransientModel):
    _name = 'wizard.standard'

    standard_id = fields.Many2one(comodel_name='standard', string='Standard_id', required=False)
    active_ids = fields.Many2many(comodel_name='vertical.stage', string='Active_ids')


    def action_insertar(self):

        # Comprobar que las fases a las que se va a agregar el standar sean partidas
        for active in self.active_ids:
            if active.type_stage_id.is_end != True:
                raise ValidationError('Debe seleccionar solo partidas')

        for active in self.active_ids:

            for line in self.standard_id.line_ids:
                items = self.env['vertical.item'].create({
                    'vertical_stage_id': active.id,
                    'project_id': active.project_id.id,
                    'cost_price': line.cost_price,
                    'product_id': line.product_id.id,
                    'uom_id': line.uom_id.id,
                    'product_qty': line.qty,
                    'descripcion': line.descripcion,
                    'job_type': line.job_type,
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
