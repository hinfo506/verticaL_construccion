from odoo import fields, models, api


class VerticalStage(models.Model):
    _name = 'vertical.stage'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ###### DATOS PRINCIPALES  ########
    # number = fields.Char(string='Number', required=True, copy=False, readonly='True',
    #                      default=lambda self: self.env['ir.sequence'].next_by_code('secuencia.partidas'))
    numero_fase = fields.Char(string='Número Fase', required=False, track_visibility='always')
    name = fields.Char(string='Nombre Fase', required=True)
    name_complete = fields.Char(string='Nombre Completo', required=True)
    descripcion = fields.Text('Descripción de la Partida')
    cantidad = fields.Integer('Cantidad', default=1)
    fecha_inicio = fields.Date('Fecha Inicio')
    fecha_finalizacion = fields.Date('Acaba el')

    total = fields.Float('Importe Total')
    # total = fields.Float('Importe Total', compute='_compute_total_parti')
    # total_prevision = fields.Float('Importe Total Previsto')

    # Campo de Prueba para poder aprobar o no aprobar
    estado_fase = fields.Selection(
        string='Estado_partida',
        selection=[('borrador', 'Borrador'),
                   ('aprobada', 'Aprobada en Prevision'),
                   ('aprobadaproceso', 'Aprobada en Proceso'),
                   ('pendiente', 'Pdte Validar'),
                   ('noaprobada', 'No aprobada'), ],
        required=False, default='borrador')

    # Item
    item_ids = fields.One2many(comodel_name='vertical.item', inverse_name='vertical_stage_id', string='Items', )
    project_id = fields.Many2one(comodel_name='project.project', string='Proyecto', required=False)

    # Calculos Generales
    material_total = fields.Float(string='Total Coste Materiales', compute='_amount_all', readonly='True')
    labor_total = fields.Float(string='Total Coste Mano de Obra', readonly='True')
    machinerycost_total = fields.Float(string='Total Coste Maquinaria', readonly='True')
    overhead_total = fields.Float(string='Total Costes Generales', readonly='True')
    jobcost_total = fields.Float(string='Total Coste', readonly='True')

    @api.depends('item_ids')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = material_total = 0.0
            for line in order.item_ids:
                # amount_untaxed += 1
                # amount_untaxed += line.price_subtotal
                material_total += line.suma_impuesto_item_y_cost_price
            order.update({
                # 'amount_untaxed': amount_untaxed,
                'material_total': material_total,
                # 'amount_total': amount_untaxed + amount_tax,
                # 'amount_total': amount_untaxed,
            })

    item_count = fields.Integer(string='Contador Item', compute='get_item_count')

    def get_item_count(self):
        for r in self:
            r.item_count = self.env['vertical.item'].search_count([('vertical_stage_id', '=', self.id)])

    def action_view_item(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Items',
            'res_model': 'vertical.item',
            'view_mode': 'tree,form',
            # 'domain': [('partidas_id', '=',  self.id)],
            'domain': [('id', 'in', self.item_ids.ids)],
            'views': [(self.env.ref('project_vertical_building.item_view_tree').id, 'tree'),
                      (self.env.ref('project_vertical_building.item_view_form').id, 'form')],
            'context': dict(self._context, default_vertical_stage_id=self.id,
                            default_project_id=self.project_id.id),
        }

    parent_id = fields.Many2one(comodel_name='vertical.stage', string='Depende de', required=False)

    child_ids = fields.One2many(comodel_name='vertical.stage', inverse_name='parent_id', string='Childs', required=False)

    type_stage_id = fields.Many2one(comodel_name='vertical.stage.type', string='Tipo de Fase', required=False)

    related_is_end = fields.Boolean('Cantidad existente', related="type_stage_id.is_end")

    def action_view_childs(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Childs',
            'res_model': 'vertical.stage',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.child_ids.ids)],
            # 'views': [(self.env.ref('project_vertical_building.item_view_tree').id, 'tree'),
            #           (self.env.ref('project_vertical_building.item_view_form').id, 'form')],
            'context': dict(self._context, default_parent_id=self.id),
        }



