# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char()
    middle_name = fields.Char()
    last_name = fields.Char()
