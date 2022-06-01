# -*- coding: utf-8 -*-
{
    'name': "Standard Requests",
    'summary': """
    
    """,

    'description': """
    
    """,

    'author': "GrowIT",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'stock', 'purchase_requisition'],
    'data': [
       
        'views/views.xml',
        'views/purchase_requisition.xml',
        'views/ir_config_settings.xml',
        'data/sequence.xml',
        #'data/standard.edificio.csv',
        #'data/standard.piso.csv',
         'security/groups.xml',
         'views/standard_report.xml',
        'security/ir.model.access.csv',
    ],
}
