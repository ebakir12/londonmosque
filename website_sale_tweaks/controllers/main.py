# -*- coding: utf-8 -*-

from odoo import api
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleExtend(WebsiteSale):

    @api.model
    def _remove_field(self, field_list, field):
        res = field_list
        try:
            res.remove(field)
        except:
            pass
        return res

    def _get_mandatory_billing_fields(self):
        """ Change original field list:
            ["name", "email", "street", "city", "country_id"] """
        result = super(WebsiteSaleExtend, self)._get_mandatory_billing_fields()
        if not request.website.use_billing_address_email:
            self._remove_field(result, 'email')
        if not request.website.use_billing_address_street:
            self._remove_field(result, 'street')
        if not request.website.use_billing_address_city:
            self._remove_field(result, 'city')
        if not request.website.use_billing_address_country:
            self._remove_field(result, 'country_id')
        return result

    def _get_mandatory_shipping_fields(self):
        """ Change original field list:
            ["name", "street", "city", "country_id"] """
        result = super(WebsiteSaleExtend, self)._get_mandatory_shipping_fields()
        if not request.website.use_shipping_address_street:
            self._remove_field(result, 'street')
        if not request.website.use_shipping_address_city:
            self._remove_field(result, 'city')
        if not request.website.use_shipping_address_country:
            self._remove_field(result, 'country_id')
        return result
