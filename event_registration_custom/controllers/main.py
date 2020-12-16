# -*- coding: utf-8 -*-

from odoo import fields, http, _
from odoo.http import request


class WebsiteEventAttendee(http.Controller):

    def check_registrations(self,emails,event):
        repeated_mails = []
        for email in emails:
            registrations = request.env['event.registration'].sudo().search([('event_id','=',event.id),('email','=',email)])
            if event.event_group_id.num_repeated_registerations and len(registrations) >= event.event_group_id.num_repeated_registerations:
                repeated_mails.append(email)
        return repeated_mails

    def check_other_registrations(self,emails,event):
        repeated_mails = []
        for email in emails:
            event_group = event.event_group_id
            registrations = request.env['event.registration'].sudo().search([('event_id.event_group_id','=',event_group.id),('email','=',email)])
            events = registrations.mapped('event_id') | event
            if event_group.restrict_num_regis and event_group.num_resgitrations < len(events):
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
        other_mails = self.check_other_registrations(emails,event)
        return {
            'emails': repeated_mails,
            'other_mails': other_mails,
            'answers':invalid_answers,
            'num_repeated_registerations': event.event_group_id.num_repeated_registerations or 1,
            'num_resgitrations': event.event_group_id.num_resgitrations or 1 ,
            'event_group': event.event_group_id.name ,
        }
