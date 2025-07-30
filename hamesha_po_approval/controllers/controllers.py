# -*- coding: utf-8 -*-
# from odoo import http


# class HameshaPoApproval(http.Controller):
#     @http.route('/hamesha_po_approval/hamesha_po_approval', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hamesha_po_approval/hamesha_po_approval/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hamesha_po_approval.listing', {
#             'root': '/hamesha_po_approval/hamesha_po_approval',
#             'objects': http.request.env['hamesha_po_approval.hamesha_po_approval'].search([]),
#         })

#     @http.route('/hamesha_po_approval/hamesha_po_approval/objects/<model("hamesha_po_approval.hamesha_po_approval"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hamesha_po_approval.object', {
#             'object': obj
#         })

