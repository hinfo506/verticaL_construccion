from odoo import fields, models, api


class VerticalStage(models.Model):
    _inherit = 'vertical.stage'

    itemcost_count = fields.Integer(string='Itemcost_count', required=False, compute='get_item_cost_count')

    def get_item_cost_count(self):
        for r in self:
            r.itemcost_count = self.env['vertical.item'].search_count([("id", "in", self.item_ids.ids), ("type_item", "=", 'cost_analysis')])
            # r.item_count = len(r.item_ids)

    def action_view_item_cost(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Items",
            "res_model": "vertical.item",
            "view_mode": "tree,form",
            # 'domain': [('partidas_id', '=',  self.id)],
            "domain": [("id", "in", self.item_ids.ids), ("type_item", "=", 'cost_analysis')],
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
