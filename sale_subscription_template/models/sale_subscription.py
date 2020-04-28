# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)


class SaleSubscriptionAlert(models.Model):
    _inherit = 'sale.subscription.alert'

    def _configure_filter_domain(self):
        for alert in self:
            domain = []
            if alert.subscription_template_ids:
                domain += [('template_id', 'in', alert.subscription_template_ids.ids)]
            if alert.customer_ids:
                domain += [('partner_id', 'in', alert.customer_ids.ids)]
            if alert.company_id:
                domain += [('company_id', '=', alert.company_id.id)]
            if alert.mrr_min:
                domain += [('recurring_monthly', '>=', alert.mrr_min)]
            if alert.mrr_max:
                domain += [('recurring_monthly', '<=', alert.mrr_max)]
            if alert.product_ids:
                # NEW change to remove product_tmpl_id
                # template_ids = alert.product_ids.mapped('product_tmpl_id.subscription_template_id').ids
                template_ids = alert.product_ids.mapped('subscription_template_id').ids
                domain += [('template_id', 'in', template_ids)]
            if alert.mrr_change_amount:
                if alert.mrr_change_unit == 'percentage':
                    domain += [('kpi_%s_mrr_percentage' % (alert.mrr_change_period), '>', alert.mrr_change_amount / 100)]
                else:
                    domain += [('kpi_%s_mrr_delta' % (alert.mrr_change_period), '>', alert.mrr_change_amount)]
            if alert.rating_percentage:
                domain += [('percentage_satisfaction', alert.rating_operator, alert.rating_percentage)]
            if alert.stage_to_id:
                domain += [('stage_id', '=', alert.stage_to_id.id)]
            super(SaleSubscriptionAlert, alert).write({'filter_domain': domain})