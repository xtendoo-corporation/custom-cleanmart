{
    'name': 'Cleanmart Assistance Kiosk',
    'version': '18.0',
    'summary': 'Kiosko de asistencias personalizado para Cleanmart',
    'author': 'Abraham (Xtendoo)',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'depends': ['hr_attendance', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/assistance_kiosk_config_views.xml',
        'views/assistance_kiosk_menu.xml',
        'views/assistance_kiosk_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/custom-cleanmart/cleanmart_assistance_kiosk/static/src/public_kiosk/cleanmart_kiosk_app.js',
        ],
    },
    'installable': True,
    'application': True,
}
