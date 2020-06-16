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
    'depends': ['event','website_event'],

    # always loaded
    'data': [
        'views/event.xml',
        'views/templates.xml',
    ],

}