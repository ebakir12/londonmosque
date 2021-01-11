# -*- coding: utf-8 -*-
from pytz import timezone
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)


class Event(models.Model):
    _inherit = 'event.event'

    event_product_ids = fields.One2many(comodel_name="event.event.product", inverse_name="event_id", )
    donation_target = fields.Float()
    show_fundraising = fields.Boolean(string="",  )

    def get_event_data(self):
        date_now = datetime.now(timezone(self._context.get('tz', self.date_tz) or self.env.user.tz)).strftime('%B %d, %Y %I:%M %p')
        products = self.event_product_ids.mapped('product_id')
        multipliers = {}
        for evp in self.event_product_ids:
            multipliers[evp.product_id] = evp.multiplier

        sale_order_lines = self.env['sale.order.line'].search([
            ('product_id','in',products.ids),
            ('order_id.state','in',('sale','done')),
        ])
        partners = sale_order_lines.mapped('order_id.partner_id')
        total = sum([ multipliers[l.product_id] * l.price_subtotal for l in sale_order_lines ])
        raise_percent = 100.0 * total / self.donation_target if self.donation_target else 0
        data = {
            'date_now': date_now,
            'total': total,
            'target': self.donation_target,
            'raise_percent': raise_percent,
            'donors': len(partners),
        }
        return data


class EventProducts(models.Model):
    _name = 'event.event.product'
    _description = 'Event Products'

    event_id = fields.Many2one(comodel_name="event.event", required=True,ondelete='cascade' )
    product_id = fields.Many2one(comodel_name="product.product", required=True,ondelete='cascade' )
    multiplier = fields.Integer(required=True, )