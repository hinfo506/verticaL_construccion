# -*- coding: utf-8 -*-
{
    'name': "Project Vertical Purchase",

    'summary': """
        Project Vertical Purchase""",

    'description': """
        Project Vertical Purchase
    """,

    'author': "OdooNext: Raul Rolando Jardinot Gonzalez",
    'website': "http://www.odoonext.com",

    'category': 'Uncategorized',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project_vertical_building', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/menu.xml',
        'views/view_purchase_order.xml',
        'views/view_item_inherit.xml',
    ],
}