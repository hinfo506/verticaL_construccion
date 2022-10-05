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
    'depends': ['base', 'project_vertical_building', 'purchase'],

    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/menu.xml',
        'views/view_purchase_order.xml',
        'views/view_item_inherit.xml',
        'views/view_stage_inherit.xml',
    ],
}
