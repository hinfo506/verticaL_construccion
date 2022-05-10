from odoo import fields, models, api
from odoo.exceptions import ValidationError


class CambioPrecioMasivo(models.TransientModel):
    _name = 'cambio.precio'

    name = fields.Char()

    nuevo_precio = fields.Float(string='Nuevo Coste', required=False)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product_id',
        required=False)

    # module_ids = env['ir.module.module'].search([('name', 'in', module_list), ('state', '=', 'uninstalled')])

    capitulos_id = fields.Many2one(comodel_name='capitulo.capitulo', string='Capitulos_id', required=False)
    project_id = fields.Many2one(comodel_name='project.project', string='Project_id', required=False)

    project_ids = fields.Many2many(
        comodel_name='project.project',
        string='Project_id')

    item_ids = fields.One2many(
        comodel_name='item.capitulo',
        inverse_name='capitulo_id',
        string='Item_ids',
        required=False, compute='_ocalcu')


    # aki tengo los item que pertenecen a ese proyecto
    # @api.onchange('product_id')
    def _ocalcu(self):
        items = self.env['item.capitulo'].search([('project_id', '=', self.project_id.id)])
        # raise ValidationError(items)
        return items