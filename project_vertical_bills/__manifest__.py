# -*- coding: utf-8 -*-
{
    'name': "Vertical Bills",

    'summary': """
        Vertical Bills""",

    'description': """
        Vertical Bills
    """,

    'author': "Raul Rolando Jardinot Gonzalez",
    'website': "http://odoonext.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project_vertical_building'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/stage_view_inherit.xml',
    ],
}