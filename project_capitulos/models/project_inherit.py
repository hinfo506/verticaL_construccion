from odoo import fields, models, api
from collections import defaultdict
from odoo.exceptions import UserError, ValidationError


class ProyectosInherit(models.Model):
    _inherit = 'project.project'

    # DATOS PRINCIPALES
    numero_proyecto = fields.Char(string=u'Número proyecto', readonly=True, default='New')

    # FASES DEL PROYECTO
    capitulos_id = fields.One2many(comodel_name='capitulo.capitulo', inverse_name='project_id', string='Capitulos_id', required=False)
    item_ids = fields.One2many(comodel_name='item.capitulo', inverse_name='project_id', string='Item_ids', required=False)

    # CONTADORES
    capitulos_count = fields.Integer(string='Capitulos', compute='get_count_capitulos')
    
    capitulos_kanban_count = fields.Integer(string='Capitulos_kanban_count', compute='_compute_capitulo_count', required=False)
    subcapitulos_kanban_count = fields.Integer(string='Subcapitulos_kanban_count', compute='_compute_subcapitulo_count', required=False)
    partidas_kanban_count = fields.Integer(string='Partidas_kanban_count', compute='_compute_partidas_count', required=False)
    item_kanban_count = fields.Integer(string='Item_kanban_count', compute='_compute_item_count', required=False)

    @api.model
    def create(self, vals):
        if vals.get('numero_proyecto', '1') == '1':
            vals['numero_proyecto'] = self.env['ir.sequence'].next_by_code('secuencia.proyecto') or '1'
        result = super(ProyectosInherit, self).create(vals)
        return result

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

    def met_subcapitulos(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subcapitulos',
            'res_model': 'sub.capitulo',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.capitulos_id.subcapitulo_ids.ids)],
            'context': dict(self._context, default_project_id=self.id),
        }

    def met_partidas(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Partidas',
            'res_model': 'partidas.partidas',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.capitulos_id.subcapitulo_ids.partidas_ids.ids)],
            'context': dict(self._context, default_project_id=self.id),
        }

    def met_items(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Items',
            'res_model': 'item.capitulo',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.capitulos_id.subcapitulo_ids.partidas_ids.item_capitulo_ids.ids)],
            'context': dict(self._context, default_project_id=self.id),
        }

    def met_activi_proyecto(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Actividades',
            'res_model': 'mail.activity',
            'view_mode': 'kanban,tree,form',
            'domain': [('res_id', '=',  self.id),('res_model','=','project.project')],
        }



    ######################
    #### Actividades #####
    ######################
    activi_count = fields.Integer(string='Contador Actividades', compute='get_acti_count')

    def get_acti_count(self):
        for r in self:
            count = self.env['mail.activity'].search_count([('res_id', '=', self.id),('res_model','=','project.project')])
            r.activi_count = count if count else 0
    ######################
    #         
    def _compute_capitulo_count(self):
        task_data = self.env['capitulo.capitulo'].read_group(
            [('project_id', 'in', self.ids)],
            ['project_id', 'project_id:count'], ['project_id'])
        result_with_subtasks = defaultdict(int)
        for data in task_data:
            result_with_subtasks[data['project_id'][0]] += data['project_id_count']
        for project in self:
            project.capitulos_kanban_count = result_with_subtasks[project.id]

    def _compute_subcapitulo_count(self):
        task_data = self.env['sub.capitulo'].read_group(
            [('project_id', 'in', self.ids)],
            ['project_id', 'project_id:count'], ['project_id'])
        result_with_subtasks = defaultdict(int)
        for data in task_data:
            result_with_subtasks[data['project_id'][0]] += data['project_id_count']
        for project in self:
            project.subcapitulos_kanban_count = result_with_subtasks[project.id]

    def _compute_partidas_count(self):
        task_data = self.env['partidas.partidas'].read_group(
            [('project_id', 'in', self.ids)],
            ['project_id', 'project_id:count'], ['project_id'])
        result_with_subtasks = defaultdict(int)
        for data in task_data:
            result_with_subtasks[data['project_id'][0]] += data['project_id_count']
        for project in self:
            project.partidas_kanban_count = result_with_subtasks[project.id]

    def _compute_item_count(self):
        task_data = self.env['item.capitulo'].read_group(
            [('project_id', 'in', self.ids)],
            ['project_id', 'project_id:count'], ['project_id'])
        result_with_subtasks = defaultdict(int)
        for data in task_data:
            result_with_subtasks[data['project_id'][0]] += data['project_id_count']
        for project in self:
            project.item_kanban_count = result_with_subtasks[project.id]

    def wizard_cambio_precio(self):
        return {
            'name': 'Cambiar Precio Masivo desde Proyecto',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cambio.precio',
            'context': {
                'default_project_id': self.id,
                'default_is_vacio': True,
                'default_info': "LOS PRECIOS SERAN CAMBIADOS A PARTIR DE </br><strong>"+str(self.name)+" :</strong>",
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = self.name + "(copia)"

        record = super(ProyectosInherit, self).copy(default)
        for capitulo in self.capitulos_id:
            record.capitulos_id |= capitulo.copy()

        return record

    def action_duplicar_proyecto(self):
        yourproject_id = self.id
        copia = self.env['project.project'].browse(yourproject_id).copy()

        return {
            'name': 'Proyecto',
            'res_model': 'project.project',
            'res_id': copia.id,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {'form_view_initial_mode': 'edit'},
        }