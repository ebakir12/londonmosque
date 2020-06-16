# -*- coding: utf-8 -*-

import babel.dates
import re
import werkzeug
from werkzeug.datastructures import OrderedMultiDict

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import fields, http, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request
from odoo.tools.misc import get_lang
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.website_event_sale.controllers.main import WebsiteEventSaleController


class WebsiteEventControllerInherit(WebsiteEventSaleController):

    def check_registrations(self,registrations,event):
        emails_tickets = []
        repeated_mails = []
        for reg in registrations:
            email = reg.get('email')
            ticket_id = int(reg.get('ticket_id'))
            key = (email,ticket_id)
            if key not in emails_tickets:
                emails_tickets.append(key)
            else:
                repeated_mails.append(email)
                continue
            registrations = request.env['event.registration'].sudo().search([('event_id','=',event.id),('email','=',email)])
            if registrations:
                repeated_mails.append(email)
        return repeated_mails

    @http.route()
    def registration_confirm(self, event, **post):
        registrations = self._process_registration_details(post)
        invalid_registrations = self.check_registrations(registrations,event)
        if invalid_registrations:
            return self.registration_new(event, **post)
        order = request.website.sale_get_order(force_create=1)
        attendee_ids = set()

        for registration in registrations:
            ticket = request.env['event.event.ticket'].sudo().browse(int(registration['ticket_id']))
            cart_values = order.with_context(event_ticket_id=ticket.id, fixed_price=True)._cart_update(product_id=ticket.product_id.id, add_qty=1, registration_data=[registration])
            attendee_ids |= set(cart_values.get('attendee_ids', []))

        # free tickets -> order with amount = 0: auto-confirm, no checkout
        if not order.amount_total:
            order.action_confirm()  # tde notsure: email sending ?
            attendees = request.env['event.registration'].browse(list(attendee_ids)).sudo()
            # clean context and session, then redirect to the confirmation page
            request.website.sale_reset()
            urls = event._get_event_resource_urls()
            return request.render("website_event.registration_complete", {
                'attendees': attendees,
                'event': event,
                'google_url': urls.get('google_url'),
                'iCal_url': urls.get('iCal_url')
            })

        return request.redirect("/shop/checkout")

# class WebsiteEventControllerInherit(WebsiteEventSaleController):
#
#     @http.route(['''/event/<model("event.event", "[('website_id', 'in', (False, current_website_id))]"):event>/registration/confirm'''], type='http', auth="public", methods=['POST'], website=True)
#     def registration_confirm(self, event, **post):
#         if not event.can_access_from_current_website():
#             raise werkzeug.exceptions.NotFound()
#
#         Attendees = request.env['event.registration']
#         registrations = self._process_registration_details(post)
#
#         for registration in registrations:
#             registration['event_id'] = event
#             attendee_values = Attendees._prepare_attendee_values(registration)
#             # try:
#             #     self.check_attendee_values(attendee_values)
#             # except Exception as e:
#             #     return request.render()
#             Attendees += Attendees.sudo().create(attendee_values)
#
#         urls = event._get_event_resource_urls()
#         return request.render("website_event.registration_complete", {
#             'attendees': Attendees.sudo(),
#             'event': event,
#             'google_url': urls.get('google_url'),
#             'iCal_url': urls.get('iCal_url')
#         })


