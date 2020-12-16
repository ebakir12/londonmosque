# -*- coding: utf-8 -*-
{
    'name': "Website Event Registration Custom",

    'summary': """
        Website Event Registration Custom""",

    'description': """
        Website Event Registration Custom
    """,

    'author': "Mahmoud Naguib",

    # for the full list
    'category': 'website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['event','event_sale','website_event','website_event_questions'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/event.xml',
        'views/templates.xml',
        'views/event_group.xml',
    ],

}