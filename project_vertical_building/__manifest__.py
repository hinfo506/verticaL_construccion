# -*- coding: utf-8 -*-
{
    'name': "project_vertical_building",

    'summary': """
        project_vertical_building""",

    'description': """
        project_vertical_building
    """,

    'author': "OdooNext",
    'website': "http://www.odoonext.com",

    'category': 'Project Management',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ["project", "stock", 'sh_activities_management_basic', 'base_setup', 'mail'],

    # always loaded
    'data': [
        # security
        'security/ir.model.access.csv',
        # views
        'views/project_inherit.xml',
        'views/view_fase.xml',
        'views/view_item.xml',
        'views/sequence.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}