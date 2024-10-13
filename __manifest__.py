{
    'name': 'To Do App',
    'technical_name': 'todo_management',
    'description': 'a simple to do app',
    'author': 'abdallah zyada',
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base', 'contacts', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/tasks_view.xml',
        'wizard/assign_task_wizard.xml',
        'reports/task_report.xml',
    ],
    'application': True
}