# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Website(models.Model):
    _inherit = "website"

    use_billing_address_email = fields.Boolean(
        string='E-mail',
        default=True,
    )
    use_billing_address_phone = fields.Boolean(
        string='Phone',
        default=True,
    )
    use_billing_address_street = fields.Boolean(
        string='Street',
        default=True,
    )
    use_billing_address_street2 = fields.Boolean(
        string='Street 2',
        default=True,
    )
    use_billing_address_city = fields.Boolean(
        string='City',
        default=True,
    )
    use_billing_address_zip = fields.Boolean(
        string='Zip Code',
        default=True,
    )
    use_billing_address_state = fields.Boolean(
        string='State',
        default=True,
    )
    use_billing_address_country = fields.Boolean(
        string='Country',
        default=True,
    )
    default_billing_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Default Country',
        default=lambda self: self.env.ref('base.public_partner').country_id,
    )

    use_shipping_address_phone = fields.Boolean(
        string='Shipping Phone',
        default=True,
    )
    use_shipping_address_street = fields.Boolean(
        string='Shipping Street',
        default=True,
    )
    use_shipping_address_street2 = fields.Boolean(
        string='Shipping Street 2',
        default=True,
    )
    use_shipping_address_city = fields.Boolean(
        string='Shipping City',
        default=True,
    )
    use_shipping_address_zip = fields.Boolean(
        string='Shipping Zip Code',
        default=True,
    )
    use_shipping_address_state = fields.Boolean(
        string='Shipping State',
        default=True,
    )
    use_shipping_address_country = fields.Boolean(
        string='Shipping Country',
        default=True,
    )

    @api.onchange('shop_ppg')
    def _onchange_shop_ppg(self):
        for website in self:
            if website.shop_ppg <= 0:
                return {
                    'value': {'shop_ppg': 20},
                    'warning': {'title': "Warning", 'message': "The value must be positive", 'type': 'notification'},
                }

    @api.onchange('shop_ppr')
    def _onchange_shop_ppr(self):
        for website in self:
            if website.shop_ppr <= 0:
                return {
                    'value': {'shop_ppr': 4},
                    'warning': {'title': "Warning", 'message': "The value must be positive", 'type': 'notification'},
                }

    @api.onchange('use_billing_address_street')
    def _onchange_use_billing_address_street(self):
        for website in self:
            if not website.use_billing_address_street:
                website.use_billing_address_street2 = False

    def write(self, vals):
        result = super(Website, self).write(vals)
        if vals.get('default_billing_country_id') or vals.get('default_billing_country_id') == False:
            self.env.ref('base.public_partner').country_id = vals.get('default_billing_country_id')
        return result
