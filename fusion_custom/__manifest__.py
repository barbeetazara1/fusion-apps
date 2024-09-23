# -*- coding: utf-8 -*-
{
    'name': "Fusion Custom",

    'summary': "Fusion Custom General",

    'description': """
        Fusion Custom For General
    """,

    'author': "My Company",
    'website': "https://internal-fusion-erp.site",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web', 'base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/login_page.xml',
        'views/users/res_users_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'fusion_custom/static/src/scss/login_page.scss',
        ],
    }
}

