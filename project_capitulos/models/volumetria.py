from odoo import fields, models, api


class Volumetria(models.Model):
    _name = 'volumetria.volumetria'

    color_linea_volumetria = fields.Selection(
        selection=[('red', 'Rojo'),
                   ('blue', 'Azul'),
                   ('green', 'Verde'),
                   ('grey', 'Gris'),
                   ('brown', 'Marrón'),
                   ('purple', 'Púrpura')],
        string="Color de la Linea",
        required=False, )

    descripcion_volumetria = fields.Text(string="Descripción volumetría", required=False)
    cantidad_volumetria = fields.Float(string='Cantidad Volumetría', required=False)
    longitud_volumetria = fields.Float(string='Longitud Volumetría', required=False)
    ancho_volumetria = fields.Float(string='Ancho Volumetría', required=False)
    alto_volumetria = fields.Float(string='Alto Volumetría', required=False)
    precio_coste_volumetria = fields.Float(string='Precio Coste Volumetría', required=False)

    total = fields.Float(string='Total', required=False, compute='_compute_total')
    partida_id = fields.Many2one(comodel_name='partidas.partidas', string='Partida', required=False)

    @api.depends('cantidad_volumetria', 'longitud_volumetria', 'ancho_volumetria', 'alto_volumetria', 'precio_coste_volumetria')
    def _compute_total(self):
        self.total = self.cantidad_volumetria * (self.longitud_volumetria * self.ancho_volumetria * self.alto_volumetria) * self.precio_coste_volumetria