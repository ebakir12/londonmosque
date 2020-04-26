# -*- coding: utf-8 -*-

# Copyright (C) 2020 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'eCommerce Tweaks',
    'version': '13.0.1.0.0',
    'category': 'eCommerce',
    'author': 'Garazd Creation',
    'website': "https://garazd.biz",
    'license': 'LGPL-3',
    'summary': 'Define billing and shipping address fields, change shop grid, set the default country.',
    'images': ['static/description/banner.png'],
    'live_test_url': 'https://demo.garazd.biz/web?db=ecommerce',
    'description': """
        Configure eCommerce:
        - change mandatory billing and shipping fields on the eCommerce Address form;
        - change shop grid;
        - set the default country.
    """,
    'depends': [
        'website_sale',
    ],
    'data': [
        'views/website_views.xml',
        'views/website_sale_templates.xml',
    ],
    'external_dependencies': {
    },
    'price': 25.0,
    'currency': 'EUR',
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
