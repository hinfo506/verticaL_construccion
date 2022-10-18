# -*- coding: utf-8 -*-
{
    'name': "project_vertical_standard",

    'summary': """
        project_vertical_standard""",

    'description': """
        project_vertical_standard
    """,

    'author': "OdooNext: raul Rolando Jardinot Gonzalez",
    'website': "http://www.odoonext.com",

    'category': 'Uncategorized',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project_vertical_cost_analysis'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/view_standar.xml',
        'views/menu.xml',
    ],
}