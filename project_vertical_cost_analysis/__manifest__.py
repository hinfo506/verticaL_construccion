# -*- coding: utf-8 -*-
{
    'name': "project_vertical_cost_analysis",

    'summary': """
        project_vertical_cost_analysis""",

    'description': """
        project_vertical_cost_analysis
    """,

    'author': "OdooNext: Raul Rolando Jardinot Gonzalez",
    'website': "http://www.odoonext.com",

    'category': 'Uncategorized',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project_vertical_building', 'standard_requests'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/view_cost_analysis.xml',
        'views/view_stage.xml',
        'views/menu.xml',
    ],
}