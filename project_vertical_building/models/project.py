from collections import defaultdict

from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    is_building = fields.Boolean()

    # DATOS PRINCIPALES

    abreviatura_proyecto = fields.Char(string='Abreviatura Proyecto', required=False)
    number = fields.Char(string='Number', required=True, copy=False, readonly='True',
                         default=lambda self: self.env['ir.sequence'].next_by_code('secuencia.proyecto'))
    numero_proyecto = fields.Char(string='Número proyecto', required=False, readonly=True,
                                  compute='compute_numero_proyecto')
    nombre_fase = fields.Char(string='Nombre Fase Principal', required=False, default='Fase Inicial')
    # Totales
    total = fields.Float('Importe Total')
    total_prevision = fields.Float('Importe Total Previsto', readonly=True)

    # Almacen
    warehouse_id = fields.Many2one(comodel_name='stock.warehouse', string='Almacén', required=False)
    stock_location_id = fields.Many2one(comodel_name='stock.location', string='Ubicación Stock', required=False)
    supervisor_id = fields.Many2one(comodel_name='res.users', string='Supervisor de almacén', required=False)

    # Fecha real de inicio y fin
    date_start_real = fields.Date(string='Date_start_real', required=False)
    date_end_real = fields.Date(string='Date_start_real', required=False)

    # Contabilidad
    invoice_address_id = fields.Many2one(comodel_name='res.partner', string='Dirección de Facturación', required=False)
    analitic_id = fields.Many2one(comodel_name='account.analytic.account', string='Cuenta Analítica', required=False)

    # Datos secundarios
    retention = fields.Float(string='Retención %', required=False)
    currency = fields.Many2one(comodel_name='res.currency', string='Moneda', required=False)
    surface = fields.Float(string='Superficie m2', required=False)
    importe_m2 = fields.Float(string='Importe m2', required=False)
    hh_planned = fields.Float(string='HH planificado', required=False)

    @api.depends('abreviatura_proyecto', 'number')
    def compute_numero_proyecto(self):
        for record in self:
            record.numero_proyecto = str(record.abreviatura_proyecto) + "-" + record.number

    # FASES DEL PROYECTO
    vertical_stage_ids = fields.One2many(comodel_name='vertical.stage', inverse_name='project_id',
                                         string='vertical_stage_ids', required=False)
    item_ids = fields.One2many(comodel_name='vertical.item', inverse_name='project_id', string='Item_ids',
                               required=False)

    item_kanban_count = fields.Integer(string='Item_kanban_count', compute='_compute_item_count', required=False)

    def action_view_fase(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.name,  # Nombre del proyecto,
            'res_model': 'vertical.stage',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.vertical_stage_ids.ids)],
            'context': dict(self._context, default_project_id=self.id, searchpanel_project_building_name=self.name,
                            project_id=self.id),
        }

    def action_view_items_tree(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.name,  # Nombre del proyecto,
            'res_model': 'vertical.item',
            'view_mode': 'tree,form',
            'domain': [('vertical_stage_id', 'in', self.vertical_stage_ids.ids)],
            'context': dict(self._context, default_project_id=self.id, searchpanel_project_building_name=self.name,
                            project_id=self.id),
        }

    def met_items(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Items',
            'res_model': 'vertical.item',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.item_ids.ids)],
            'context': dict(self._context, default_project_id=self.id),
        }

    fase_kanban_count = fields.Integer(string='FasePrincipal_kanban_count', compute='_compute_fase_count',
                                       required=False)

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

    def _compute_fase_count(self):
        task_data = self.env['vertical.stage'].read_group(
            [('project_id', 'in', self.ids)],
            ['project_id', 'project_id:count'], ['project_id'])
        result_with_subtasks = defaultdict(int)
        for data in task_data:
            result_with_subtasks[data['project_id'][0]] += data['project_id_count']
        for project in self:
            project.fase_kanban_count = result_with_subtasks[project.id]

    def _compute_item_count(self):
        task_data = self.env['vertical.item'].read_group(
            [('project_id', 'in', self.ids)],
            ['project_id', 'project_id:count'], ['project_id'])
        result_with_subtasks = defaultdict(int)
        for data in task_data:
            result_with_subtasks[data['project_id'][0]] += data['project_id_count']
        for project in self:
            project.item_kanban_count = result_with_subtasks[project.id]

    ##############################################################################################
    # Se captura el momento en el que el proyecto pasa de estado en prevision y captura el total #
    ##############################################################################################
    def write(self, values):

        if values.get('stage_id'):
            stage = self.sudo().env['project.project.stage'].search([('id', '=', values.get('stage_id'))])
            if not stage.is_prevision and self.total_prevision == 0:
                values['total_prevision'] = self.total
                return super(ProjectProject, self).write(values)
            else:
                return super(ProjectProject, self).write(values)
        else:
            return super(ProjectProject, self).write(values)
