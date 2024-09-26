from odoo import models, fields, api, _

class ProductInventoryLine(models.Model):
    _name = 'product.inventory.line'
    _description = "Inventory Product Cost"

    product_template_id = fields.Many2one('product.template')
    product_id = fields.Many2one('product.product', string=_('Product'), domain=[('detailed_type', '=', 'product')])
    qty = fields.Float('Quantity')
    uom_id = fields.Many2one('uom.uom', string=_('Uom'), related='product_id.uom_id')
