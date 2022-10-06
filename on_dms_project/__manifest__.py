# -*- coding: utf-8 -*-
{
    'name': "on_dms_project",

    'summary': """
        on_dms_project""",

    'description': """
        on_dms_project
    """,

    'author': "OdooNext: Raul Rolando Jardinot Gonzalez",
    'category': 'Uncategorized',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'dms', 'project_vertical_building'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_inherit.xml',
        'views/view_capitulo.xml',
        'views/view_subcapitulo.xml',
        'views/directory_inherit_view.xml',
        'views/view_inherit_partida.xml',
        'views/view_fase_principal.xml',
    ],

}
