from odoo import fields, models, api
from collections import defaultdict
from odoo.exceptions import UserError, ValidationError


class ProyectosInherit(models.Model):
    _inherit = 'project.project'

    capitulos_id = fields.One2many(comodel_name='capitulo.capitulo', inverse_name='project_id', string='Capitulos_id', required=False)
    capitulos_count = fields.Integer(string='Capitulos', compute='get_count_capitulos')
    item_ids = fields.One2many(comodel_name='item.capitulo', inverse_name='project_id', string='Item_ids', required=False)

    def get_count_capitulos(self):
        for r in self:
            count = self.env['capitulo.capitulo'].search_count([('project_id', '=', self.id)])
            r.capitulos_count = count if count else 0


    def met_capitulos(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Capitulos',
            'res_model': 'capitulo.capitulo',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.capitulos_id.ids)],
            'context': dict(self._context, default_project_id=self.id),
        }

    capitulos_kanban_count = fields.Integer(string='Capitulos_kanban_count', compute='_compute_capitulo_count', required=False)
    
    def _compute_capitulo_count(self):
        task_data = self.env['capitulo.capitulo'].read_group(
            [('project_id', 'in', self.ids)],
            ['project_id', 'project_id:count'], ['project_id'])
        result_with_subtasks = defaultdict(int)
        for data in task_data:
            result_with_subtasks[data['project_id'][0]] += data['project_id_count']
        for project in self:
            project.capitulos_kanban_count = result_with_subtasks[project.id]

    def wizard_cambio_precio(self):
        return {
            'name': 'Cambiar Precio Masivo desde Proyecto',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cambio.precio',
            'context': {
                'default_project_id': self.id,
                'default_info': "LOS PRECIOS SERAN CAMBIADOS A PARTIR DE AQUI EN ADELANTE: <strong>PROYECTO/CAPITULO/SUBCAPITULO/PARTIDA</strong>",
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }