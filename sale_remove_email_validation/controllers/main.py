# -*- coding: utf-8 -*-

from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleInherited(WebsiteSale):

    def _get_mandatory_billing_fields(self):
        return ["name", "street", "city", "country_id"]
