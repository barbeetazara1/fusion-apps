# -*- coding: utf-8 -*-
# from odoo import http


# class FusionCustom(http.Controller):
#     @http.route('/fusion_custom/fusion_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fusion_custom/fusion_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('fusion_custom.listing', {
#             'root': '/fusion_custom/fusion_custom',
#             'objects': http.request.env['fusion_custom.fusion_custom'].search([]),
#         })

#     @http.route('/fusion_custom/fusion_custom/objects/<model("fusion_custom.fusion_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fusion_custom.object', {
#             'object': obj
#         })

