# -*- coding: utf-8 -*-
{
    "name": "Cleanmart Assistances Custom",
    "version": "1.0",
    "category": "Human Resources",
    "summary": "Personalizaciones para asistencias en Cleanmart",
    "author": "xtendoo",
    "depends": ["hr", "hr_attendance"],
    "data": [
        "views/hr_department_views.xml",
        "views/hr_employee_views.xml",
    ],
    "assets": {
        "hr_attendance.assets_public_attendance": [
            "cleanmart_assistances_custom/static/src/xml/manual_selection_no_all.xml",
            "cleanmart_assistances_custom/static/src/js/kiosk_patch.js",
        ],
    },
    "installable": True,
    "application": False,
}
