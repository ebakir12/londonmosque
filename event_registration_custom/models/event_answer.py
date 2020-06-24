# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)

default = "With this answer, you are not eligible to Register."

class EventAnswer(models.Model):
    _inherit = 'event.answer'

    prevent_submit = fields.Boolean()


class EventQuestion(models.Model):
    _inherit = 'event.question'

    wrong_answer_text = fields.Char(default=default )

    @api.model
    def set_default_wrong_answer_text(self):
        questions = self.env['event.question'].search([('wrong_answer_text','=',False)])
        for q in questions:
            q.write({'wrong_answer_text': default})

