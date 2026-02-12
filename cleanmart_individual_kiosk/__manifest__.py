{
    'name': 'Cleanmart Individual Kiosk',
    'version': '19.0.1.0.0',
    'summary': 'Kiosco de asistencias individual para un único empleado',
    'description': """
        Kiosco Individual de Asistencias
        =================================
        Permite a empleados individuales registrar asistencias mediante:
        - URL única por empleado
        - Vista tipo kiosco (sin navegación)
        - Validación por PIN
        - Diseño mobile-first
        - Múltiples empleados pueden tener su propio kiosco individual
    """,
    'author': 'Abraham (Xtendoo)',
    'website': 'https://www.xtendoo.es',
    'license': 'LGPL-3',
    'category': 'Human Resources/Attendances',
    'depends': [
        'hr_attendance',
    ],
    'data': [
        'views/hr_employee_views.xml',
        'views/kiosk_individual_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'cleanmart_individual_kiosk/static/src/css/kiosk_individual.css',
            'cleanmart_individual_kiosk/static/src/js/kiosk_individual.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
