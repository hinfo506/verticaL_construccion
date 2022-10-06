# -*- coding: utf-8 -*-
{
    "name": "ON CHANGE PRODUCT",
    "summary": """
        ON CHANGE PRODUCT""",
    "description": """
        ON CHANGE PRODUCT
    """,
    "author": "Odoo Next",
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "project_capitulos"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/view_subcapitulo_inherit.xml",
        "views/view_partida_inherit.xml",
        "views/view_faseprincipal_inherit.xml",
        "views/view_capitulo_inherit.xml",
        "wizard/view_change_product.xml",
        "views/view_project_inherit.xml",
    ],
}
