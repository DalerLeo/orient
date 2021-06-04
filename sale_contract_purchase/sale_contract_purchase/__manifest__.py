# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Sale Contract: Purchase',
    'version': '14.0.1',
    'category': 'Purchase',
    'summary': 'Contract for Purchase',

    'author': 'Colibri',
    'website': 'https://clbr.uz',
    'depends': [
        'sale_contract',
        'purchase'
    ],
    'data': [
        'views/sale_contract_views.xml',
    ],
    'qweb': [
    ],
    'application': True,
}
