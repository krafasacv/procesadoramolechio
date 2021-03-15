# -*- coding: utf-8 -*-

from odoo import models, fields, api

class procesadora(models.Model):
     _inherit = 'account.invoice'
     x_idorigen = fields.Integer('id de origen')
     x_estado_de_promocion = fields.Char('Estado de Promoción', default='Sin Promoción')
     x_con_promocion = fields.Boolean('Tiene Promoción?', default=False)
     x_estado_de_copia = fields.Char('Estado de la Copia', default='Sin Copiar')
     x_se_copia = fields.Boolean('Se copia?', default=False)
     x_prueba = fields.Char('para pruebas')
     

     @api.multi
     def prueba(self):
          for x in self:
               x.x_prueba = x.x_prueba + self.number


     @api.multi
     def pruebas(self):
          self.x_prueba = self.number


     @api.multi
     def boton_fv3_ncv3(self):
          dic = {'type': 'out_refund',
          'x_prueba': self.partner_id.id,
          'partner_id': self.partner_id.id,
          'date_invoice': self.date_invoice,
          'date_due': self.date_due,
          'payment_term_id': self.payment_term_id.id,
          'user_id': self.user_id.id,
          'origin': self.number,
          'x_idorigen': self.id,
          'x_estado_de_promocion': 'No aplica'
          }

          idnew = self.env['account.invoice'].create(dic)
          self.env.cr.commit()
          self.x_prueba = dic
          ppromo = self.env['product.product'].search([('product_tmpl_id','=',3317)])


          for x in self.invoice_line_ids:
              promo = 0
              if str(x['product_id'].default_code)[:3] == 'MOL':
                   if x.quantity > 19:
                        dic2 = {'quantity': int(x.quantity/20),
                                'product_id': ppromo.id,
                                'name': 'Promocion 1 en 20 del producto ' + x.name,
                                'account_id': 472,
                                'price_unit': x.price_unit,
                                'discount': x.discount,
                                'x_studio_precio_con_descuento': x.x_studio_precio_con_descuento,
                                'invoice_id': idnew.id,
                                }
                   idnews = self.env['account.invoice.line'].create(dic2)
                   env.cr.commit()

          self['x_estado_de_promocion'] = 'Esperando Validación'
          #record['x_studio_pruebas'] = 'nuevo id de factura: ' + str(idnew) + 'nuevo id de lineas: ' + str(idnews)

     @api.multi
     def boton_fv1_fv3(self):
         record = self
         cia = 3
         if record.partner_id.vat:
             cliente = env['res.partner'].sudo().search(
                 ['&', '&', ('company_id', '=', cia), ('vat', '=', record.partner_id.vat), ('customer', '=', 'TRUE')])[0]
         else:
             cliente = env['res.partner'].sudo().search(
                 ['&', '&', ('company_id', '=', cia), ('vat', '=', 'XAXX010101000'), ('customer', '=', 'TRUE')])[0]
         
         dic = {'type': record.type,
                #'x_studio_pruebas': '',
                'partner_id': cliente.id,
                'date_invoice': record.date_invoice,
                'date_due': record.date_due,
                'date': record.date,
                'payment_term_id': cliente.property_payment_term_id.id,
                'user_id': user.id,
                'x_idorigen': record.id,
                'company_id': cia,
                'journal_id': 27,  # de donde se puedo tomar este dato ?????
                'create_uid': user.id,
                'write_uid': user.id,
                'partner_shipping_id': cliente.id,
                'x_estado_de_promocion': 'Sin promoción'
                }

         idnew = self.env['account.invoice'].sudo().create(dic)
         self.env.cr.commit()

         pida = 0  # producto id anterior

         for x in record.invoice_line_ids:
             ptid2 = self.env['product.product'].sudo().search(['&', ('product_tmpl_id.company_id', '=', cia), (
             'default_code', '=', x.product_id.product_tmpl_id.default_code)])
             if pida != x.product_id.id:
                 pida = x.product_id.id
                 precio = x.price_unit
                 descuento = x.discount
                 precio_con_descuento = x.x_studio_precio_con_descuento

             dic2 = {'quantity': x.quantity,
                     'product_id': ptid2.id,
                     'name': x.name,
                     'account_id': 412,  # hay un error cuando se obtiene la cuenta contable del cliente
                     'price_unit': precio,  
                     'discount': descuento, 
                     'x_studio_precio_con_descuento': precio_con_descuento,  
                     'invoice_id': idnew.id,
                     'company_id': cia,
                     }
             self.env['account.invoice.line'].sudo().create(dic2)
             self.env.cr.commit()

         record['x_estado_de_copia'] = 'Copiado en Borrador'

     @api.multi
     def boton_fv1_so3(self):
         record = self
         cia = 3
         if record.partner_id.vat:
             cliente = self.env['res.partner'].sudo().search(['&', '&', ('company_id', '=', cia), ('vat', '=', record.partner_id.vat),
                                                             ('customer', '=', 'TRUE')])[0]
         else:
             cliente = self.env['res.partner'].sudo().search(['&', '&', ('company_id', '=', cia), ('vat', '=', 'XAXX010101000'),
                                                              ('customer', '=', 'TRUE')])[0]
             
         dic = {
             'x_studio_pruebas': '',
             'partner_id': cliente.id,
             'partner_invoice_id': cliente.id,
             'partner_shipping_id': cliente.id,
             'date_order': record.date_invoice,
             'payment_term_id': cliente.property_payment_term_id.id,
             'user_id': user.id,
             'x_studio_idinvoice1': record.id,
             'company_id': cia,
             'create_uid': user.id,
             'write_uid': user.id,
             'state': 'draft',
             'warehouse_id': 5
             }

         idnew = self.env['sale.order'].sudo().create(dic)
         self.env.cr.commit()

         pida = 0  # producto id anterior

         for x in record.invoice_line_ids:
             ptid2 = self.env['product.product'].sudo().search(['&', ('product_tmpl_id.company_id', '=', cia),
                                                    ('default_code', '=', x.product_id.product_tmpl_id.default_code)])

             if pida != x.product_id.id:
                 pida = x.product_id.id
                 precio = x.price_unit
                 descuento = x.discount
                 precio_con_descuento = x.x_studio_precio_con_descuento

             dic2 = {
                 'order_id': idnew.id,
                 'name': x.product_id.product_tmpl_id.name,
                 'invoice_status': 'no',
                 'price_unit': precio,
                 'price_subtotal': x.quantity * precio,
                 'price_tax': 0.00,
                 'price_total': x.quantity * precio,
                 'price_reduce': precio,
                 'price_reduce_taxinc': precio,
                 'price_reduce_taxexcl': precio,
                 'discount': descuento,  # x.discount,
                 'product_id': ptid2.id,
                 'product_uom_qty': x.quantity,
                 'product_uom': x.product_id.product_tmpl_id.uom_id.id,
                 'company_id': cia,
                 }

             self.env['sale.order.line'].sudo().create(dic2)
             self.env.cr.commit()

         record['x_estado_de_copia'] = 'Copiado en Borrador'

    #esta parte es para que cuando se valide la copia le devuelva el numero al que fue copiada la factura
     @api.multi
     def regreso_fv1_fv3(self):
         record = self
         fe1 = self.env['account.invoice'].sudo().search([('id','=',record.x_idorigen)])
         fe1['x_studio_estado_de_copia'] = record.move_id.name

     @api.multi
     def regreso_fv3_ncv3(self):
         record = self
         fe1 = self.env['account.invoice'].sudo().search([('id','=',record.x_studio_idinvoice1)])
         fe1['x_studio_estado_de_promocion'] = record.move_id.name

