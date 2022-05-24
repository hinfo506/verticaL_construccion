from odoo import fields, models, api
from collections import defaultdict
from odoo.exceptions import UserError, ValidationError


class FaseInicial(models.Model):
    _name = 'fase.principal'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()

    number = fields.Char(string='Number', required=True, copy=False, readonly='True',
                         default=lambda self: self.env['ir.sequence'].next_by_code('secuencia.faseprincipal'))

    # FASES DEL PROYECTO
    project_id = fields.Many2one(comodel_name='project.project', string='Proyecto', required=False)
    capitulos_ids = fields.One2many(comodel_name='capitulo.capitulo', inverse_name='fase_principal_id', string='Capitulos_id', required=False)
    # item_ids = fields.One2many(comodel_name='item.capitulo', inverse_name='project_id', string='Item_ids', required=False)

    numero_fase_principal = fields.Char(string='Numero Fase Principal', required=False)

    @api.onchange('number', 'project_id')
    def _onchange_join_number_faseprincipal(self):
        self.numero_fase_principal = str(self.project_id.numero_proyecto) + "." + str(self.number)



    def met_capitulos(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Capitulos',
            'res_model': 'capitulo.capitulo',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.capitulos_ids.ids)],
            'context': dict(self._context, default_fase_principal_id=self.id),
        }

    cap_count = fields.Integer(string='Capitulos', compute='get_count_capitulos')

    def get_count_capitulos(self):
        for r in self:
            count = self.env['capitulo.capitulo'].search_count([('fase_principal_id', '=', self.id)])
            r.cap_count = count if count else 0

    ######################
    #### Actividades #####
    ######################
    activi_count = fields.Integer(string='Contador Actividades', compute='get_acti_count')

    def get_acti_count(self):
        for r in self:
            count = self.env['mail.activity'].search_count(
                [('res_id', '=', self.id), ('res_model', '=', 'fase.principal')])
            r.activi_count = count if count else 0

    def met_activi_capitulos(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Actividades',
            'res_model': 'mail.activity',
            'view_mode': 'kanban,tree,form',
            'domain': [('res_id', '=', self.id), ('res_model', '=', 'fase.principal')],
        }