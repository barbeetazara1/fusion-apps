from odoo import models, fields, api, _
from datetime import timedelta, datetime


class ResUsers(models.Model):
    _inherit = 'res.users'

    trial_day = fields.Date('Trial Date', default=lambda self: datetime.today() + timedelta(days=14))

    def cron_auto_archive(self):
        pass