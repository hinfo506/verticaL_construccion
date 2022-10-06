# -*- coding: utf-8 -*-
{
    'name': "project_capitulos_purchase",

    'summary': """
        project_capitulos_purchase""",

    'description': """
        project_capitulos_purchase
    """,

    'author': "OdooNext: Raul Rolando Jardinot Gonzalez",
    'website': "http://www.odoonext.com",
    'category': 'Uncategorized',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project_capitulos', 'purchase'],

    # always loaded
    'data': [
        'views/partidas_views.xml',
    ],
}
