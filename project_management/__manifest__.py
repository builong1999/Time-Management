# Copyright © 2021 Novobi, LLC
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Project Management',
    'summary': 'Project Management',
    'category': 'Project',
    "author": "Drake Bui",
    "website": "https://www.drakebui.ml/",
    "depends": ['hr', 'digest'],
    "data": [
        'data/project_data.xml',
        'data/digest_email_template.xml',
        'data/system_data.xml',

        'security/jira_security.xml',
        'security/ir.model.access.csv',

        'views/board_board_views.xml',
        'views/hr_employee_views.xml',
        'views/jira_project_views.xml',
        'views/jira_ticket_views.xml',
        'views/jira_status_views.xml',
        'views/jira_type_views.xml',
        'views/jira_time_logging_views.xml',
        'views/digest_email_views.xml',

        'views/menus.xml',

        'wizard/jira_logging_time_views.xml',
        'wizard/kick_off_counting_views.xml',
    ],
    "application": True,
    'assets': {
        'web.assets_backend': [
            'project_management/static/**/*',
        ],
    }
}
