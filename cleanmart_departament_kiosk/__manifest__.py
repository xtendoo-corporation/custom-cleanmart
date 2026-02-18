{
    'name': 'Cleanmart Department Kiosk',
    'version': '19.0.1.0.0',
    'summary': 'Kiosco de asistencias por departamento',
    'description': """
        Kiosco de Asistencias por Departamento
        ========================================
        Permite configurar un kiosco de asistencias para todos los empleados de un departamento.
        - URL única por departamento
        - Selección de empleado desde una lista
        - Validación por PIN
        - Diseño profesional Cleanmart
    """,
    'author': 'Abraham (Xtendoo)',
    'website': 'https://www.xtendoo.es',
    'license': 'LGPL-3',
    'category': 'Human Resources/Attendances',
    'depends': [
        'hr_attendance',
    ],
    'data': [
        'views/hr_department_views.xml',
        'views/kiosk_department_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'cleanmart_departament_kiosk/static/src/css/kiosk_department.css',
            'cleanmart_departament_kiosk/static/src/js/kiosk_department.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
