from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_inventory_line = fields.One2many('product.inventory.line', 'product_template_id')