# -*- coding: utf-8 -*-
{
    'name': "on_activity_directory",

    'summary': """
        on_activity_directory""",

    'description': """
        on_activity_directory
    """,

    'author': "Raul Rolando Jardinot Gonzalez",

    'category': 'Uncategorized',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sh_activities_management_basic', 'dms'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/dms_directory_inherit_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
