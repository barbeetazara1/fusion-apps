from odoo import models, fields, api, _
from datetime import timedelta, datetime


class ResUsers(models.Model):
    _inherit = 'res.users'

    trial_day = fields.Date('Trial Date', default=lambda self: datetime.today() + timedelta(days=14))

    @api.model
    def _auto_archive_users(self):
        today = fields.Date.today()
        users_to_archive = self.search([('trial_day', '<=', today), ('active', '=', True)])
        
        for user in users_to_archive:
            user.write({'active': False})