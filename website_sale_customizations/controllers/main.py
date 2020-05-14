# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from werkzeug.exceptions import Forbidden, NotFound
from odoo import fields, models, api, _
from odoo import tools
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging

LOGGER = logging.getLogger(__name__)


class WebsiteSaleInherited(WebsiteSale):

    def _get_mandatory_billing_fields(self):
        return ["name", "first_name", "last_name", "street", "city", "country_id"]

    def _get_mandatory_shipping_fields(self):
        return ["name", "first_name", "last_name", "street", "city", "country_id"]

    def checkout_form_validate(self, mode, all_form_values, data):
        # mode: tuple ('new|edit', 'billing|shipping')
        # all_form_values: all values before preprocess
        # data: values after preprocess
        error = dict()
        error_message = []
        first_name = data.get('first_name','')
        last_name = data.get('last_name','')
        middle_name = data.get('middle_name','')
        name = first_name + ' ' + middle_name + ' ' + last_name
        all_form_values.update({'name':name})
        data.update({'name':name})
        # Required fields from form
        required_fields = [f for f in (all_form_values.get('field_required') or '').split(',') if f]
        # Required fields from mandatory field function
        required_fields += mode[1] == 'shipping' and self._get_mandatory_shipping_fields() or self._get_mandatory_billing_fields()
        # Check if state required
        country = request.env['res.country']
        if data.get('country_id'):
            country = country.browse(int(data.get('country_id')))
            if 'state_code' in country.get_address_fields() and country.state_ids:
                required_fields += ['state_id']

        # error message for empty required fields
        for field_name in required_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        Partner = request.env['res.partner']
        if data.get("vat") and hasattr(Partner, "check_vat"):
            if data.get("country_id"):
                data["vat"] = Partner.fix_eu_vat_number(data.get("country_id"), data.get("vat"))
            partner_dummy = Partner.new({
                'vat': data['vat'],
                'country_id': (int(data['country_id'])
                               if data.get('country_id') else False),
            })
            try:
                partner_dummy.check_vat()
            except ValidationError:
                error["vat"] = 'error'

        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        return error, error_message

    def _checkout_form_save(self, mode, checkout, all_values):
        Partner = request.env['res.partner']
        if mode[0] == 'new':
            if checkout and checkout.get('phone'):
                phone = checkout.get('phone')
                Partner = Partner.sudo().search([('phone','=',phone)],limit=1)
                partner_id = Partner.id
                if not Partner:
                    partner_id = Partner.sudo().create(checkout).id
        elif mode[0] == 'edit':
            partner_id = int(all_values.get('partner_id', 0))
            if partner_id:
                # double check
                order = request.website.sale_get_order()
                shippings = Partner.sudo().search([("id", "child_of", order.partner_id.commercial_partner_id.ids)])
                if partner_id not in shippings.mapped('id') and partner_id != order.partner_id.id:
                    return Forbidden()
                Partner.browse(partner_id).sudo().write(checkout)
        return partner_id



