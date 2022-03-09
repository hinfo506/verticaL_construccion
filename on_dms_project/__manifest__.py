# -*- coding: utf-8 -*-
{
    'name': "on_dms_project",

    'summary': """
        on_dms_project""",

    'description': """
        on_dms_project
    """,

    'author': "Raul Rolando Jardinot Gonzalez",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'dms', 'project_capitulos'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_inherit.xml',
    ],

}