# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Fund Raising',
    'category': 'Website/Website',
    'summary': 'Fund Raising',
    'version': '1.0',
    'description': """
    Fund Raising
    """,
    'depends': ['website','product','website_sale','event_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/event_event.xml',
    ],
    'installable': True,
}
