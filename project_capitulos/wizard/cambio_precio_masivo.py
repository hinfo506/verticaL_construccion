from odoo import fields, models, api


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


