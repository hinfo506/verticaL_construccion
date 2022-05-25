from odoo import fields, models, api
from collections import defaultdict
from odoo.exceptions import UserError, ValidationError


class ProyectosInherit(models.Model):
    _inherit = 'project.project'

    # DATOS PRINCIPALES
    # numero_proyecto = fields.Char(string=u'Número proyecto', readonly=True, default='New')
    number = fields.Char(string='Number', required=True, copy=False, readonly='True',
                         default=lambda self: self.env['ir.sequence'].next_by_code('secuencia.proyecto'))
    numero_proyecto = fields.Char(string='Número proyecto', required=False, readonly=True)


    abreviatura_proyecto = fields.Char(string='Abreviatura Proyecto', required=False)
    nombre_fase = fields.Char(string='Nombre_fase', required=False, default='Fase Inicial')

    @api.onchange('number', 'abreviatura_proyecto')
    def _onchange_join_number_proyecto(self):
        self.numero_proyecto = str(self.abreviatura_proyecto) + "-" + str(self.number)

    # FASES DEL PROYECTO
    fase_principal_ids = fields.One2many(comodel_name='fase.principal', inverse_name='project_id', string='Fase_principal_ids', required=False)
    capitulos_id = fields.One2many(comodel_name='capitulo.capitulo', inverse_name='project_id', string='Capitulos_id', required=False)
    item_ids = fields.One2many(comodel_name='item.capitulo', inverse_name='project_id', string='Item_ids', required=False)
    # partidas_ids = fields.One2many(comodel_name='partidas.partidas', inverse_name='project_id',string='Partidas_ids', required=False)
    # subcapitulos_ids = fields.One2many(comodel_name='sub.capitulo', inverse_name='project_id', string='Subcapitulos_ids', required=False)

    # CONTADORES
    capitulos_count = fields.Integer(string='Capitulos', compute='get_count_capitulos')
    fases_principal_count = fields.Integer(string='Fases contador', compute='get_count_fases_principal')

    fase_principal_kanban_count = fields.Integer(string='FasePrincipal_kanban_count', compute='_compute_faseprincipal_count', required=False)
    capitulos_kanban_count = fields.Integer(string='Capitulos_kanban_count', compute='_compute_capitulo_count', required=False)
    subcapitulos_kanban_count = fields.Integer(string='Subcapitulos_kanban_count', compute='_compute_subcapitulo_count', required=False)
    partidas_kanban_count = fields.Integer(string='Partidas_kanban_count', compute='_compute_partidas_count', required=False)
    item_kanban_count = fields.Integer(string='Item_kanban_count', compute='_compute_item_count', required=False)

    # @api.model
    # def create(self, vals):
    #     if vals.get('numero_proyecto', '1') == '1':
    #         vals['numero_proyecto'] = self.env['ir.sequence'].next_by_code('secuencia.proyecto') or '1'
    #     result = super(ProyectosInherit, self).create(vals)
    #     return result

    def get_count_capitulos(self):
        for r in self:
            count = self.env['capitulo.capitulo'].search_count([('project_id', '=', self.id)])
            r.capitulos_count = count if count else 0

    def get_count_fases_principal(self):
        for r in self:
            count = self.env['fase.principal'].search_count([('project_id', '=', self.id)])
            r.fases_principal_count = count if count else 0


    def met_fase_principal(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Fase Inicial',
            'res_model': 'fase.principal',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.fase_principal_ids.ids)],
            'context': dict(self._context, default_project_id=self.id),
        }

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
    
    def _compute_faseprincipal_count(self):
        task_data = self.env['fase.principal'].read_group(
            [('project_id', 'in', self.ids)],
            ['project_id', 'project_id:count'], ['project_id'])
        result_with_subtasks = defaultdict(int)
        for data in task_data:
            result_with_subtasks[data['project_id'][0]] += data['project_id_count']
        for project in self:
            project.fase_principal_kanban_count = result_with_subtasks[project.id]

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
        copia_proyecto = self.env['project.project'].browse(yourproject_id).copy()
        self.env.cr.commit()
        for proyecto in copia_proyecto:
            for capitulo_id in proyecto.capitulos_id:
                capitulo_id.subcapitulo_ids.write({'project_id': copia_proyecto.id, 'capitulo_id': capitulo_id.id})
                for subcapitulo_id in capitulo_id.subcapitulo_ids:
                    subcapitulo_id.partidas_ids.write({'project_id': copia_proyecto.id, 'capitulo_id': capitulo_id.id})
                    for partidas_id in subcapitulo_id.partidas_ids:
                        partidas_id.item_capitulo_ids.write({'project_id': proyecto.id, 'capitulo_id': capitulo_id.id, 'subcapitulo_id': subcapitulo_id.id})
                        partidas_id.item_capitulo_materiales_ids.write({'project_id': proyecto.id, 'capitulo_id': capitulo_id.id, 'subcapitulo_id': subcapitulo_id.id})
                        partidas_id.item_mano_obra_ids.write({'project_id': proyecto.id, 'capitulo_id': capitulo_id.id, 'subcapitulo_id': subcapitulo_id.id})
                        partidas_id.item_capitulo_gastos_generales.write({'project_id': proyecto.id, 'capitulo_id': capitulo_id.id, 'subcapitulo_id': subcapitulo_id.id})
                        partidas_id.item_capitulo_maquinaria.write({'project_id': proyecto.id, 'capitulo_id': capitulo_id.id, 'subcapitulo_id': subcapitulo_id.id})
                        partidas_id.volumetria_ids.write({'project_id': proyecto.id, 'capitulo_id': capitulo_id.id, 'subcapitulo_id': subcapitulo_id.id})

        return {
            'name': 'Proyecto',
            'res_model': 'project.project',
            'res_id': copia_proyecto.id,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {'form_view_initial_mode': 'edit'},
        }