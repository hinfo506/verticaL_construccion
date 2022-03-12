# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': "Activities Management Basic | All In One Schedule Activities | Activity Dashboard | Advance Schedule Activity | Dynamic Action For Multiple Activities | Activity Management Dashboard | Activities Dashboard",
    'author' : 'Softhealer Technologies',
    'website': 'https://www.softhealer.com',
    "support": "support@softhealer.com",
    'category': 'Discuss',
    'version': '15.0.1',
    "summary": "Activity Scheduler Employee Activity Supervisor Activity filter Activity Multi Activity Schedule Mass Activity Tag activity history Activity monitoring Activity multi users assign schedule activity schedule activities Multi Company Activity Mail Odoo",
    "description": """Do you want to show the well-organized structure of activities? Do you want to show completed, uncompleted activities easily to your employees? Do you want to show an activity dashboard to the employee? Do you want to show the scheduled activity to the manager, supervisor & employee? This module helps the manager can see everyone's activity, the supervisor can see the assigned user and their own activity, the user can see only their own activity. You can see activities like all activities, planned activities, completed activities, or overdue activities. Manager, Supervisor & Employee have their own dashboard. Activity notification will help to send a notification before and after the activity due date. You can notify your salesperson/customer before or after the activity is done. Hurray!""",
    'depends': [
        'mail',
    ],
    'data': [
        'security/activity_security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/activity_config_setting.xml',
        'wizard/feedback.xml',
        'wizard/mark_as_done.xml',
        'views/activity_views.xml',
        'views/activity_dashboard.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sh_activities_management_basic/static/src/css/crm_dashboard.css',
            'sh_activities_management_basic/static/src/js/action_manager_act_window.js',
            'sh_activities_management_basic/static/src/js/activity_dashboard.js',
            ],
        'web.assets_qweb': [
            'sh_activities_management_basic/static/src/xml/**/*',
        ],
    },
    'images': ['static/description/background.png', ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "license": "OPL-1",
    "price": 50,
    "currency": "EUR"
}
