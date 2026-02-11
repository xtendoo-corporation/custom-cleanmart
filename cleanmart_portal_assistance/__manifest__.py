{
    'name': 'Cleanmart Portal Assistance',
    'version': '19.0.1.0.0',
    'summary': 'Portal de asistencias personal para empleados de Cleanmart',
    'description': """
        Portal Personal de Asistencias
        ================================
        Permite a los empleados gestionar sus propias asistencias desde el portal:
        - Check In/Check Out personal
        - Visualización de estado actual
        - Historial de asistencias
        - Estadísticas de horas trabajadas
        - Interfaz moderna y responsive
    """,
    'author': 'Abraham (Xtendoo)',
    'website': 'https://www.xtendoo.es',
    'license': 'LGPL-3',
    'category': 'Human Resources/Attendances',
    'depends': [
        'hr_attendance',
        'portal',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/portal_attendance_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'cleanmart_portal_assistance/static/src/css/portal_attendance.css',
            'cleanmart_portal_assistance/static/src/js/portal_attendance.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
