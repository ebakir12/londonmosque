# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)


class Event(models.Model):
    _inherit = 'event.event'

    hide_price = fields.Boolean()
    # hide_qty = fields.Boolean()
    event_group_id = fields.Many2one(comodel_name="event.group",)

class EventReg(models.Model):
    _inherit = 'event.registration'

    @api.model
    def _prepare_attendee_values(self, registration):
        first_name = registration.get('first_name','')
        last_name = registration.get('last_name','')
        name = first_name + ' ' + last_name
        registration['name'] = name
        return super(EventReg,self)._prepare_attendee_values(registration)
