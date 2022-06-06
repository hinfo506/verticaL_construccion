# -*- coding: utf-8 -*-
{
    'name': "On ADD Standar",

    'summary': """
        On ADD Standar""",

    'description': """
        On ADD Standar
    """,

    'author': "Odoo Next",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'standard_requests', 'project_capitulos'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/view_subcapitulo_inherit.xml',
        'views/view_partida_inherit.xml',
        'wizard/view_add_standar_partida.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}