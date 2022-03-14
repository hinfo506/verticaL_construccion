from odoo import fields, models, api


class MailActivities(models.Model):
    _inherit = 'mail.activity'

    directory_id = fields.Many2one(comodel_name='dms.directory', string='Directorios', required=False)
