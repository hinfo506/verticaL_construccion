from odoo import fields, models, api


class Capitulo(models.Model):
    _name = 'capitulo.capitulo'

    name = fields.Char(string='Capitulo', required=True)
    cantidad = fields.Integer('Cantidad')
    total = fields.Float('Importe Total')
    fecha_finalizacion = fields.Date('Fecha Finalización')
    project_id = fields.Many2one('project.project', string='Proyecto')
    descripcion = fields.Text('Descripción del Capitulo')

    subcapitulo_ids = fields.One2many(
        comodel_name='sub.capitulo',
        inverse_name='capitulo_id',
        string='Subcapitulos',
        required=False)
