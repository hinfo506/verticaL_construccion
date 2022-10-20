from odoo import fields, models, api
from odoo.exceptions import ValidationError


class VerticalStage(models.Model):
    _inherit = 'vertical.stage'

    itemstand_count = fields.Integer(string='Itemstand_count', required=False, compute='get_item_stand_count')

    def get_item_stand_count(self):
        for r in self:
            r.itemstand_count = self.env['vertical.item'].search_count([("id", "in", self.item_ids.ids), ("type_item", "=", 'standard')])
            # r.item_count = len(r.item_ids)

    def action_view_item_standard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Items",
            "res_model": "vertical.item",
            "view_mode": "tree,form",
            # 'domain': [('partidas_id', '=',  self.id)],
            "domain": [("id", "in", self.item_ids.ids), ("type_item", "=", 'standard')],
            # "views": [
            #     (self.env.ref("project_vertical_building.item_view_tree").id, "tree"),
            #     (self.env.ref("project_vertical_building.item_view_form").id, "form"),
            # ],
            # "context": dict(
            #     self._context,
            #     default_vertical_stage_id=self.id,
            #     default_project_id=self.project_id.id,
            # ),
        }

    def add_standars(self):
        act_ids = self.env.context.get('active_ids')
        active_ids = self.env['vertical.stage'].search([('id', '=', act_ids)])

        # Comprobar que las fases a las que se va a agregar el standar sean partidas
        for active in active_ids:
            if not active.type_stage_id.is_end:
                raise ValidationError('Debe seleccionar solo Fases de tipo Final')

        return {
            'name': 'Add Standard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.standard',
            'context': {
                'default_active_ids': act_ids,
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def add_standars_one_id(self):
        return {
            'name': 'Add Standard',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.standard',
            'context': {
                'default_active_id': self.id,
                'default_is_one': True,
            },
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
