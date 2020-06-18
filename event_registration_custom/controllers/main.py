# -*- coding: utf-8 -*-

from odoo import fields, http, _
from odoo.http import request


class WebsiteEventAttendee(http.Controller):

    def check_registrations(self,emails,event):
        repeated_mails = []
        for email in emails:
            registrations = request.env['event.registration'].sudo().search([('event_id','=',event.id),('email','=',email)])
            if registrations:
                repeated_mails.append(email)
        return repeated_mails

    def check_answers(self,answers,event):
        answers = request.env['event.answer'].sudo().browse(answers)
        invalid_answers = answers.filtered(lambda a:a.prevent_submit)
        return invalid_answers.ids

    @http.route(['''/event/<model("event.event", "[('website_id', 'in', (False, current_website_id))]"):event>/check_attendees_data'''], type='json', auth="public", methods=['POST'], website=True)
    def check_attendees_mails(self, event, **post):
        emails = post.get('emails')
        answers = post.get('answers')
        invalid_answers = self.check_answers(answers,event)
        repeated_mails = self.check_registrations(emails,event)
        return {'emails': repeated_mails,'answers':invalid_answers}
