# -*- coding: utf-8 -*-
{
    'name': "Standard Requests",
    'summary': "Standard Requests",
    'author': "OdooNext,Raul Rolando Jardinot Gonzalez",
    'website': "",
    'category': 'Uncategorized',
    'version': '15.0.1.0.0',
    'depends': ['base', 'stock', 'purchase_requisition', 'project_vertical_building'],
    'data': [
        'security/ir.model.access.csv',
        'views/view_standard.xml',
        'views/view_stage.xml',
        'wizard/view_add_standard.xml',
        'views/view_item.xml',
        'views/menu.xml',

    ],
}
