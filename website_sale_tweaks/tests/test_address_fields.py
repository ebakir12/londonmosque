# -*- coding: utf-8 -*-

import odoo.tests
from odoo import api
from odoo.addons.website_sale_tweaks.controllers.main import WebsiteSaleExtend
from odoo.addons.website_sale.tests.test_sale_process import TestWebsiteSaleCheckoutAddress
from odoo.addons.website.tools import MockRequest


@odoo.tests.tagged('post_install', '-at_install')
class TestWebsiteSaleAddressChange(TestWebsiteSaleCheckoutAddress):

    def setUp(self):
        super(TestWebsiteSaleAddressChange, self).setUp()
        self.WebsiteSaleController = WebsiteSaleExtend()

    def test_10_public_user_hide_address_fields(self):
        """ This test ensure that after hiding the billing/shipping address fields,
            partner address fields are saved properly.

            mode "new / billing":
                order.partner_id = public_user.partner_id
                kw['partner_id'] = -1
            mode "edit / billing":
                order.partner_id != public_user.partner_id
                kw['partner_id'] > 0 AND kw['partner_id'] = order.partner_id.id
            mode "new / shipping":
                order.partner_id != public_user.partner_id
                kw['partner_id'] = -1
            mode "edit / shipping":
                kw['partner_id'] > 0 AND kw['partner_id'] != order.partner_id.id
        """
        so = self._create_so(self.website.user_id.partner_id.id)
        env = api.Environment(self.env.cr, self.website.user_id.id, {})
        with MockRequest(env, website=self.website.with_env(env), sale_order_id=so.id):

            self.website.use_billing_address_email = False
            self.website.use_billing_address_phone = False
            self.website.use_billing_address_street = False
            self.website.use_billing_address_street2 = False
            self.website.use_billing_address_city = False
            self.website.use_billing_address_zip = False
            self.website.use_billing_address_state = False
            self.website.use_billing_address_country = False

            billing_address_values = {
                'partner_id': -1,
                'name': 'Billing address',
                'submitted': 1,
            }
            self.WebsiteSaleController.address(**billing_address_values)
            new_partner = so.partner_id
            self.assertNotEqual(new_partner, self.website.user_id.partner_id, "Order partner must not be the equal the public user partner.")
            self.assertFalse(new_partner.email, "Order billing email should be empty.")
            self.assertFalse(new_partner.phone, "Order billing phone should be empty.")
            self.assertFalse(new_partner.street, "Order billing street should be empty.")
            self.assertFalse(new_partner.street2, "Order billing street2 should be empty.")
            self.assertFalse(new_partner.city, "Order billing city should be empty.")
            self.assertFalse(new_partner.zip, "Order billing zip code should be empty.")
            self.assertFalse(new_partner.state_id, "Order billing state should be empty.")
            self.assertFalse(new_partner.country_id, "Order billing country should be empty.")

            self.website.use_shipping_address_phone = False
            self.website.use_shipping_address_street = False
            self.website.use_shipping_address_street2 = False
            self.website.use_shipping_address_city = False
            self.website.use_shipping_address_zip = False
            self.website.use_shipping_address_state = False
            self.website.use_shipping_address_country = False
            shipping_address_values = {
                'partner_id': -1,
                'name': 'Shipping address',
                'submitted': 1,
            }
            self.WebsiteSaleController.address(**shipping_address_values)
            new_shipping = self._get_last_address(new_partner)
            self.assertNotEqual(new_shipping, new_partner, "Order partner and shipping address must be different.")
            self.assertFalse(new_shipping.phone, "Order shipping phone should be empty.")
            self.assertFalse(new_shipping.street, "Order shipping street should be empty.")
            self.assertFalse(new_shipping.street2, "Order shipping street2 should be empty.")
            self.assertFalse(new_shipping.city, "Order shipping city should be empty.")
            self.assertFalse(new_shipping.zip, "Order shipping zip code should be empty.")
            self.assertFalse(new_shipping.state_id, "Order shipping state should be empty.")
            self.assertFalse(new_shipping.country_id, "Order shipping country should be empty.")

            self.website.use_billing_address_email = True
            self.website.use_billing_address_phone = True
            self.website.use_billing_address_city = True
            self.website.use_billing_address_street = True
            self.website.use_billing_address_street2 = True
            self.website.use_billing_address_zip = True
            self.website.use_billing_address_state = True
            self.website.use_billing_address_country = True
            billing_address_values.update({
                'partner_id': new_partner.id,
                'name': 'Billing address',
                'email': 'email@email.email',
                'phone': '0123456789',
                'street': 'ooo',
                'street2': 'uuu',
                'city': 'ABC',
                'zip': '11111',
                'state_id': self.env.ref('base.state_au_1').id,
                'country_id': self.env.ref('base.au').id,
            })
            self.WebsiteSaleController.address(**billing_address_values)
            self.assertEqual(new_partner.name, 'Billing address', "Order partner name should have a value.")
            self.assertEqual(new_partner.email, 'email@email.email', "Order billing email should have a value.")
            self.assertEqual(new_partner.phone, '0123456789', "Order billing phone should have a value.")
            self.assertEqual(new_partner.city, 'ABC', "Order billing city should have a value.")
            self.assertEqual(new_partner.street, 'ooo', "Order billing street should have a value.")
            self.assertEqual(new_partner.street2, 'uuu', "Order billing street2 should have a value.")
            self.assertEqual(new_partner.zip, '11111', "Order billing zip should have a value.")
            self.assertEqual(new_partner.state_id, self.env.ref('base.state_au_1'), "Order billing country should have a value.")
            self.assertEqual(new_partner.country_id, self.env.ref('base.au'), "Order billing country should have a value.")

            self.website.use_shipping_address_phone = True
            self.website.use_shipping_address_street = True
            self.website.use_shipping_address_street2 = True
            self.website.use_shipping_address_city = True
            self.website.use_shipping_address_zip = True
            self.website.use_shipping_address_state = True
            self.website.use_shipping_address_country = True
            shipping_address_values.update({
                'partner_id': new_shipping.id,
                'phone': '000111222',
                'street': 'eee',
                'street2': 'bbb',
                'city': 'iii',
                'zip': '22222',
                'state_id': self.env.ref('base.state_ar_s').id,
                'country_id': self.env.ref('base.ar').id,
            })
            self.WebsiteSaleController.address(**shipping_address_values)
            edit_shipping = self._get_last_address(new_partner)
            self.assertEqual(new_shipping, edit_shipping, "Partner shipping contact must be the same.")
            self.assertEqual(edit_shipping.phone, '000111222', "Order shipping phone should have a value.")
            self.assertEqual(edit_shipping.city, 'iii', "Order shipping city should have a value.")
            self.assertEqual(edit_shipping.street, 'eee', "Order shipping street should have a value.")
            self.assertEqual(edit_shipping.street2, 'bbb', "Order shipping street2 should have a value.")
            self.assertEqual(edit_shipping.zip, '22222', "Order shipping zip should have a value.")
            self.assertEqual(edit_shipping.state_id, self.env.ref('base.state_ar_s'), "Order shipping country should have a value.")
            self.assertEqual(edit_shipping.country_id, self.env.ref('base.ar'), "Order shipping country should have a value.")
