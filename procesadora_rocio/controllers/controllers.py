# -*- coding: utf-8 -*-
from odoo import http

# class ProcesadoraRocio(http.Controller):
#     @http.route('/procesadora_rocio/procesadora_rocio/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/procesadora_rocio/procesadora_rocio/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('procesadora_rocio.listing', {
#             'root': '/procesadora_rocio/procesadora_rocio',
#             'objects': http.request.env['procesadora_rocio.procesadora_rocio'].search([]),
#         })

#     @http.route('/procesadora_rocio/procesadora_rocio/objects/<model("procesadora_rocio.procesadora_rocio"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('procesadora_rocio.object', {
#             'object': obj
#         })