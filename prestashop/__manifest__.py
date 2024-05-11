# -*- coding: utf-8 -*-
{
    'name': "prestashop",

    'summary': "Import product prestashop to odoo",

    'description': """""",

    'author': "MLKA",
    'website': "https://mlka-groupe.fr/",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Product',
    'version': '17.0.1.0',
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}

