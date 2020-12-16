# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)


class EventGroup(models.Model):
    _name = 'event.group'
    _rec_name = 'name'
    _description = 'Event Group'
    _order = 'name asc, id desc'

    name = fields.Char(string="Name", required=True, )
    restrict_num_regis = fields.Boolean(string="Restrict Registrations",default=False  )
    num_resgitrations = fields.Integer(string="Number Of Registrations per Group", default=1 )
    num_repeated_registerations = fields.Integer(string="Number Of Repeated Registrations Per Event", default=1 )
