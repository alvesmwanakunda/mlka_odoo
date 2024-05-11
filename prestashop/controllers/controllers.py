# -*- coding: utf-8 -*-
# from odoo import http


# class Prestashop(http.Controller):
#     @http.route('/prestashop/prestashop', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/prestashop/prestashop/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('prestashop.listing', {
#             'root': '/prestashop/prestashop',
#             'objects': http.request.env['prestashop.prestashop'].search([]),
#         })

#     @http.route('/prestashop/prestashop/objects/<model("prestashop.prestashop"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('prestashop.object', {
#             'object': obj
#         })

