# -*- coding: utf-8 -*-
{
    'name': "Catalogo de Compra",

    'summary': """
        Purchase Catalogue""",

    'description': """
        Purchase Catalogue
    """,

    'author': "Odoonext: Raul Rolando Jardinot Gonzalez",
    'website': "http://odoonext.com",

    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project_capitulos'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/view_catalogue.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}