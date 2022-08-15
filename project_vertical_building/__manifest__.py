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
    'depends': ["web", "project", "stock", 'sh_activities_management_basic', 'base_setup', 'mail'],

    # always loaded
    'data': [
        # security
        'security/ir.model.access.csv',
        # views
        'views/project_inherit.xml',
        'views/stage_views.xml',
        'views/view_stage_type.xml',
        'views/view_item.xml',
        'views/sequence.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'project_vertical_building/static/src/xml/*',
        ],
        'web.assets_backend': [
            'project_vertical_building/static/src/js/legacy/vertical_search_panel_model_extension.js',
            'project_vertical_building/static/src/js/legacy/vertical_search_panel.js',
            'project_vertical_building/static/src/js/legacy/vertical_stage_tree.js',
            # 'project_vertical_building/static/src/js/vertical_search_panel_model_extension.js',
            # 'project_vertical_building/static/src/js/vertical_search_panel.js',
            # 'project_vertical_building/static/src/js/vertical_stage_tree.js',
        ],
    }
}