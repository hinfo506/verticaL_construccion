from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'ProjectName.TableName'
    _description = 'Description'

    name = fields.Char()
