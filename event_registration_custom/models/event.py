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