# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountInvoice(models.Model):
     _inherit = 'account.invoice'
     x_origen = fields.Char('Documento Origen')
     is_available = fields.Boolean('Is Available?')
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
