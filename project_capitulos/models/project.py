# -*- coding: utf-8 -*-

from odoo import api, fields, models
"""
i.IdProyecto
ii.Descripción del Capitulo
iii.Cantidad
iv.Importe Total
Fecha Finalización
"""


class CapituloCapitulo(models.Model):
    _name = 'capitulo.capitulo'

    name = fields.Char(string='Capitulo', required=True)
    cantidad = fields.Integer('Cantidad')
    total = fields.Float('Importe Total')
    fecha_finalizacion = fields.Date('Fecha Finalización')
    project_id = fields.Many2one('project.project', string='Proyecto')
    descripcion = fields.Text('Descripción del Capitulo')
    

"""
i.IdCapitulo
ii.Texto Descriptivo del Sub-Capitulo
iii.Importe Total
Fecha e Finalización
"""
class SubCapitulo(models.Model):
    _name = 'sub.capitulo'

    name = fields.Char(string='Sub-Capitulo', required=True)
    descripcion = fields.Text('Descripción del Sub-Capitulo')    
    total = fields.Float('Importe Total')
    fecha_finalizacion = fields.Date('Fecha Finalización')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo')


"""
c.Datos Ítem del Capitulo
i.IdSub-Capitulo
ii.Tipo de Ítem
1.Articulo
2.Mano de Obra
3.Gastos Generales
a.Aduanas
b.Transportes Terrestres
c.Transportes Marítimos
iii.Descripción del Ítem
iv.Cantidad
v.Precio Coste (Previsión de Costes)
vi.Precio Coste R2 (Revisión 2 de costes de esta línea)
vii.Precio Coste R3 (Revisión 3 de costes de esta línea)
viii.Precio Coste R4 (Revisión 4 de costes de esta línea)
ix.Precio Coste Final
x.Margen de Beneficio

"""



class ItemCapitulo(models.Model):
    _name = 'item.capitulo'

    name = fields.Char(string='Sub-Capitulo', required=True)
    descripcion = fields.Text('Descripción del Sub-Capitulo')    
    total = fields.Float('Importe Total')
    fecha_finalizacion = fields.Date('Fecha Finalización')
    capitulo_id = fields.Many2one('capitulo.capitulo', string='Capitulo')    