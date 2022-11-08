from odoo import fields, models
from odoo.exceptions import ValidationError


class VerticalCostAnalysis(models.Model):
    _name = "vertical.cost.analysis"

    name = fields.Char("Nombre")
    code = fields.Char(string="Código", required=False)
    standard_id = fields.Many2one(comodel_name="standard", string="Standard")
    cost_analysis_line_ids = fields.One2many(
        comodel_name="cost.analysis.line",
        inverse_name="cost_analysis_id",
        string="Cost_analysis_line_ids",
        required=False,
    )
    cost_standard = fields.Float(
        string="", required=False, related="standard_id.total_cost"
    )
    cost_cost_analysis = fields.Float(
        string="Total Coste", required=False, compute="_compute_amount_cost_total"
    )

    item_ids = fields.One2many(
        comodel_name="vertical.item",
        inverse_name="cost_analysis_id",
        string="Item_ids",
        required=False,
    )

    def _compute_amount_cost_total(self):
        for record in self:
            sumatoria = 0
            if record.cost_standard or record.cost_analysis_line_ids:
                sumatoria = record.cost_standard + sum(
                    c.suma_impuesto_item_y_cost_price
                    for c in record.cost_analysis_line_ids
                )
            record.cost_cost_analysis = sumatoria

    def action_throw_changes(self):
        # record.update({
        #     'precio_total': record.metros_contratados * record.espacio_id.precio_mn,
        # })
        stages_ids = self.env["vertical.stage"].search([("cost_analysis_id", "=", self.id), ("project_id.stage_id.is_prevision", "=", True)])
        # stages_ids = self.env["vertical.stage"].search([("cost_analysis_id", "=", self.id), ("project_id.stage_id.is_prevision", "=", True)]).mapped("item_cost_analysis_ids")
        # raise ValidationError(stages_ids)
        # raise ValidationError(stages_ids)
        # for sta in stages_ids:
        #     sta.item_cost_analysis_ids.unlink()
        #     sta.item_standard_ids.unlink()
        #     item_cost_analysis_ids=[]
        #     item_standard_ids=[]
        #     for line in self.cost_analysis_line_ids:
        #         item_cost_analysis_ids.append(
        #             (
        #                 1,
        #                 0,
        #                 {
        #                     "cost_analysis_id": self.id,
        #                     "project_id": sta.project_id.id,
        #                     "job_type": line.job_type,
        #                     "product_id": line.product_id.id,
        #                     "descripcion": line.descripcion,
        #                     "uom_id": line.uom_id.id,
        #                     "product_qty": line.product_qty,
        #                     "cost_price": line.cost_price,
        #                     "subtotal_item_capitulo": line.subtotal_item_capitulo,
        #                     "tipo_descuento": line.tipo_descuento,
        #                     "cantidad_descuento": line.cantidad_descuento,
        #                     "subtotal_descuento": line.subtotal_descuento,
        #                     "impuesto_porciento": line.impuesto_porciento,
        #                     "total_impuesto_item": line.total_impuesto_item,
        #                     "beneficio_estimado": line.beneficio_estimado,
        #                     "importe_venta": line.importe_venta,
        #                     "suma_impuesto_item_y_cost_price": line.suma_impuesto_item_y_cost_price,
        #                 },
        #             )
        #         )
        #     for line in self.standard_id.line_ids:
        #         item_standard_ids.append(
        #             (
        #                 1,
        #                 0,
        #                 {
        #                     "project_id": sta.project_id.id,
        #                     "standard_id": self.id.standard_id.id,
        #                     "job_type": line.job_type,
        #                     "product_id": line.product_id.id,
        #                     "descripcion": line.descripcion,
        #                     "uom_id": line.uom_id.id,
        #                     "product_qty": line.product_qty,
        #                     "cost_price": line.cost_price,
        #                     "subtotal_item_capitulo": line.subtotal_item_capitulo,
        #                     "tipo_descuento": line.tipo_descuento,
        #                     "cantidad_descuento": line.cantidad_descuento,
        #                     "subtotal_descuento": line.subtotal_descuento,
        #                     "impuesto_porciento": line.impuesto_porciento,
        #                     "total_impuesto_item": line.total_impuesto_item,
        #                     "beneficio_estimado": line.beneficio_estimado,
        #                     "importe_venta": line.importe_venta,
        #                     "suma_impuesto_item_y_cost_price": line.suma_impuesto_item_y_cost_price,
        #                 },
        #             )
        #         )
        #     sta.item_cost_analysis_ids = item_cost_analysis_ids
        #     sta.item_standard_ids = item_standard_ids

        # Probando Nuevo Metodo

        lis_add = []
        for sta in stages_ids:
            for record in sta.item_cost_analysis_ids:
                for r in self.cost_analysis_line_ids:
                    if record.product_id == r.product_id:
                        # print(str(record) + '****')
                        record.update({
                            # "cost_analysis_id": self.id,
                            # "project_id": sta.project_id.id,
                            # "job_type": line.job_type,
                            # "product_id": line.product_id.id,
                            # "descripcion": line.descripcion,
                            # "uom_id": line.uom_id.id,
                            "product_qty": r.product_qty,
                            "cost_price": r.cost_price,
                            # "subtotal_item_capitulo": line.subtotal_item_capitulo,
                            # "tipo_descuento": line.tipo_descuento,
                            # "cantidad_descuento": line.cantidad_descuento,
                            # "subtotal_descuento": line.subtotal_descuento,
                            # "impuesto_porciento": line.impuesto_porciento,
                            # "total_impuesto_item": line.total_impuesto_item,
                            # "beneficio_estimado": line.beneficio_estimado,
                            # "importe_venta": line.importe_venta,
                            # "suma_impuesto_item_y_cost_price": line.suma_impuesto_item_y_cost_price,
                        })
                    elif record.product_id != r.product_id:
                        lis_add.append(r)
                        # print(r.product_id.name)
        # for lista in lis_add:
        #     print(str(lista.product_id.name) + "  : Distinto")

        # buscar productos tdistintos

        # Todos los productos en el AC
        # for record in self.cost_analysis_line_ids.mapped("product_id"):
        #     print(str(record)+"  :producto en el AC")

        # todos los productos que hay en la fase
        # for sta in stages_ids:
        #     for record in sta.item_cost_analysis_ids.mapped("product_id"):
        #         print(str(record) + "  :producto en la fase")

        # tomar la diferencia entre el Ac y los ac agregados a la fase
        # list_diference=[]
        # for element in list1:
        #     if element not in lis2:
        #         list_diference.append(element)


        for sta in stages_ids:
            list_diference = []
            list1 = self.cost_analysis_line_ids.mapped("product_id")
            list2 = sta.item_cost_analysis_ids.mapped("product_id")
            for element in list1:
                if element not in list2:
                    list_diference.append(element)
            # print(str(list_diference) + "  lista de productos que no tiene la fase")
            # productos a agregar
            item_add = []
            for l in list_diference:
                item_add = self.cost_analysis_line_ids.search([("product_id", "=", l.id)])
            print(item_add)

