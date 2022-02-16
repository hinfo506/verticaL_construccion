# Copyright 2019 Patrick Wilson <patrickraymondwilson@gmail.com>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

{
    "name": "Project Capitulos",
    "summary": """Project Capitulos""",
    "author": "David Montero Crespo",
    "website": "https://odoonext.com",
    "category": "Project Management",
    "version": "14.0.1.1.0",
    "license": "AGPL-3",
    "depends": ["project"],
    "data": [
        'security/ir.model.access.csv',
        # "views/project.xml",
        "views/menu.xml",
        "views/view_capitulo.xml",
        "views/view_subcapitulo.xml",
        "views/project_inherit.xml",
    ],
    "application": False,
}
