# -*- coding: utf-8 -*-
{
    'name': "Standard Requests",
    'summary': """Standard Requests
    
    """,

    'description': """Standard Requests
    
    """,

    'author': "OdooNext:Raul Rolando Jardinot Gonzalez",
    'website': "",

    'category': 'Uncategorized',
    'version': '15.0.1',
    'depends': ['base', 'stock', 'purchase_requisition', 'project_vertical_building'],
    'data': [
        'security/ir.model.access.csv',
        # 'views/purchase_requisition.xml',
        # 'views/ir_config_settings.xml',
        'data/sequence.xml',
        #'data/standard.edificio.csv',
        #'data/standard.piso.csv',
        # 'views/standard_report.xml',
        'views/view_standard.xml',
        'views/view_stage.xml',
        'wizard/view_add_standard.xml',
        # 'views/view_standard_request.xml',
        # 'views/view_standard_tags.xml',
        'views/menu.xml',
        # 'security/groups.xml',

    ],
}
