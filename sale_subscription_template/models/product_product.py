# -*- coding: utf-8 -*-
""" init object """
from odoo import fields, models, api, _ , exceptions


class ProductProduct(models.Model):
    _inherit = 'product.product'

    recurring_invoice = fields.Boolean('Subscription Product',help='If set, confirming a sale order with this product will create a subscription')
    subscription_template_id = fields.Many2one('sale.subscription.template', 'Subscription Template',
        help="Product will be included in a selected template")