{
    "name": "project_vertical_building",
    "summary": """
        project_vertical_building""",
    "description": """
        project_vertical_building
    """,
    "author": "OdooNext",
    "website": "https://github.com/odoo-next/verticaL_construccion",
    "category": "Project Management",
    "version": "15.0.1",
    "depends": [
        "web",
        "project",
        "stock",
        "sh_activities_management_basic",
        "base_setup",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/project_inherit.xml",
        "views/view_stage.xml",
        "views/view_stage_type.xml",
        "views/view_item.xml",
        "views/project_stage_view_inherit.xml",
        "views/sequence.xml",
        "views/view_standard.xml",
        "views/view_standard_line.xml",
        "wizard/view_add_standard.xml",
        "wizard/view_acost_stage_wizard.xml",
        "views/view_cost_analysis.xml",
        "views/view_cost_analysis_line.xml",
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_qweb": [
            "project_vertical_building/static/src/xml/*",
        ],
        "web.assets_common": [
            "project_vertical_building/static/src/lib/bootstrap-menu.min.js",
        ],
        "web.assets_backend": [
            "project_vertical_building/static/src/js/legacy/vertical_search_panel_model_extension.js",
            "project_vertical_building/static/src/js/legacy/vertical_search_panel.js",
            "project_vertical_building/static/src/js/legacy/vertical_stage_tree.js",
            "project_vertical_building/static/src/js/psi_view/psi_view.js",
            "project_vertical_building/static/src/css/psi_view.scss",
        ],
    },
}
