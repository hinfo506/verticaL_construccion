# -*- coding: utf-8 -*-
{
    'name': "project_vertical_purchase_catalogue",

    'summary': """
        project_vertical_purchase_catalogue""",

    'description': """
        project_vertical_purchase_catalogue
    """,

    'author': "OdooNext: Raul Rolando Jardinot Gonzalez",
    'website': "http://www.odoonext.com",

    'category': 'Uncategorized',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}
