from collections import defaultdict

from odoo import fields, models, api


class ProyectosInherit(models.Model):
    _inherit = 'project.project'

    # DATOS PRINCIPALES

    numero_proyecto = fields.Char(string='Número proyecto', required=False, readonly=True,
                                  compute='_compute_numero_pryecto')
    abreviatura_proyecto = fields.Char(string='Abreviatura Proyecto', required=False)
    nombre_fase = fields.Char(string='Nombre Fase Principal', required=False, default='Fase Inicial')
    number = fields.Char(string='Number', required=True, copy=False, readonly='True',
                         default=lambda self: self.env['ir.sequence'].next_by_code('secuencia.proyecto'))
    # Totales
    total = fields.Float('Importe Total', compute='_compute_total_cap')
    total_prevision = fields.Float('Importe Total Previsto')

    warehouse = fields.Many2one(comodel_name='stock.warehouse', string='Almacén', required=False)

    @api.depends('abreviatura_proyecto', 'number')
    def _compute_numero_pryecto(self):
        self.numero_proyecto = str(self.abreviatura_proyecto) + "-" + str(self.number)

    # FASES DEL PROYECTO
    fase_principal_ids = fields.One2many(comodel_name='fase.principal', inverse_name='project_id',
                                         string='Fase_principal_ids', required=False)
    capitulos_id = fields.One2many(comodel_name='capitulo.capitulo', inverse_name='project_id', string='Capitulos_id',
                                   required=False)
    item_ids = fields.One2many(comodel_name='item.capitulo', inverse_name='project_id', string='Item_ids',
                               required=False)
    # partidas_ids = fields.One2many(comodel_name='partidas.partidas', inverse_name='project_id',string='Partidas_ids', required=False)
    # subcapitulos_ids = fields.One2many(comodel_name='sub.capitulo', inverse_name='project_id', string='Subcapitulos_ids', required=False)

    fase_principal_kanban_count = fields.Integer(string='FasePrincipal_kanban_count',
                                                 compute='_compute_faseprincipal_count', required=False)
    capitulos_kanban_count = fields.Integer(string='Capitulos_kanban_count', compute='_compute_capitulo_count',
                                            required=False)
    subcapitulos_kanban_count = fields.Integer(string='Subcapitulos_kanban_count', compute='_compute_subcapitulo_count',
                                               required=False)
    partidas_kanban_count = fields.Integer(string='Partidas_kanban_count', compute='_compute_partidas_count',
                                           required=False)
    item_kanban_count = fields.Integer(string='Item_kanban_count', compute='_compute_item_count', required=False)

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
            'domain': [('res_id', '=', self.id), ('res_model', '=', 'project.project')],
        }

    ######################
    #### Actividades #####
    ######################
    activi_count = fields.Integer(string='Contador Actividades', compute='get_acti_count')

    def get_acti_count(self):
        for r in self:
            count = self.env['mail.activity'].search_count(
                [('res_id', '=', self.id), ('res_model', '=', 'project.project')])
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
                'default_info': "LOS PRECIOS SERAN CAMBIADOS A PARTIR DE </br><strong>" + str(
                    self.name) + " :</strong>",
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
        for faseprincipal in self.fase_principal_ids:
            record.fase_principal_ids |= faseprincipal.copy()

        return record

    def action_duplicar_proyecto(self):
        yourproject_id = self.id
        copia_proyecto = self.env['project.project'].browse(yourproject_id).copy()
        self.env.cr.commit()
        for proyecto in copia_proyecto:
            for faseprincipal_id in proyecto.fase_principal_ids:
                faseprincipal_id.capitulos_ids.write({'project_id': copia_proyecto.id})
                for capitulo_id in faseprincipal_id.capitulos_ids:
                    capitulo_id.subcapitulo_ids.write({'project_id': copia_proyecto.id, 'capitulo_id': capitulo_id.id})
                    for subcapitulo_id in capitulo_id.subcapitulo_ids:
                        subcapitulo_id.partidas_ids.write(
                            {'project_id': copia_proyecto.id, 'capitulo_id': capitulo_id.id})
                        for partidas_id in subcapitulo_id.partidas_ids:
                            partidas_id.item_capitulo_ids.write(
                                {'project_id': proyecto.id, 'capitulo_id': capitulo_id.id,
                                 'subcapitulo_id': subcapitulo_id.id})
                            partidas_id.item_capitulo_materiales_ids.write(
                                {'project_id': proyecto.id, 'capitulo_id': capitulo_id.id,
                                 'subcapitulo_id': subcapitulo_id.id})
                            partidas_id.item_mano_obra_ids.write(
                                {'project_id': proyecto.id, 'capitulo_id': capitulo_id.id,
                                 'subcapitulo_id': subcapitulo_id.id})
                            partidas_id.item_capitulo_gastos_generales.write(
                                {'project_id': proyecto.id, 'capitulo_id': capitulo_id.id,
                                 'subcapitulo_id': subcapitulo_id.id})
                            partidas_id.item_capitulo_maquinaria.write(
                                {'project_id': proyecto.id, 'capitulo_id': capitulo_id.id,
                                 'subcapitulo_id': subcapitulo_id.id})
                            partidas_id.volumetria_ids.write({'project_id': proyecto.id, 'capitulo_id': capitulo_id.id,
                                                              'subcapitulo_id': subcapitulo_id.id})

        return {
            'name': 'Proyecto',
            'res_model': 'project.project',
            'res_id': copia_proyecto.id,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {'form_view_initial_mode': 'edit'},
        }

    def _compute_total_cap(self):
        for record in self:
            suma = 0.0
            for sub in record.fase_principal_ids:
                suma += sub.total
            record.update({'total': suma, })

    def write(self, values):

        if values.get('stage_id'):
            stage = self.sudo().env['project.project.stage'].search([('id', '=', values.get('stage_id'))])
            if stage.is_prevision == False and self.total_prevision == 0:
                values['total_prevision'] = self.total

                record = super(ProyectosInherit, self).write(values)

                # Fase Principal
                fase_ids = self.env['fase.principal'].search([('project_id', '=', self.id)])
                for fase in fase_ids:
                    fase.sudo().write({
                        'total_prevision': fase.total,
                    })

                # Capitulo
                capitulo_ids = self.env['capitulo.capitulo'].search([('project_id', '=', self.id)])
                for cap in capitulo_ids:
                    cap.sudo().write({
                        'total_prevision': cap.total,
                    })

                # Subcapitulo
                subcapitulos_ids = self.env['sub.capitulo'].search([('project_id', '=', self.id)])
                for sub in subcapitulos_ids:
                    sub.sudo().write({
                        'total_prevision': sub.total,
                    })

                # Partida
                partidas_ids = self.env['partidas.partidas'].search([('project_id', '=', self.id)])
                for par in partidas_ids:
                    par.sudo().write({
                        'total_prevision': par.total,
                    })

                # Item
                items_ids = self.env['item.capitulo'].search([('project_id', '=', self.id)])
                for item in items_ids:
                    item.sudo().write({
                        'total_prevision': item.suma_impuesto_item_y_cost_price,
                    })

                return record

            else:
                return super(ProyectosInherit, self).write(values)
        else:
            return super(ProyectosInherit, self).write(values)
