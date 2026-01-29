from odoo import http
from odoo.http import request

class CleanmartAssistanceKioskController(http.Controller):
    @http.route('/cleanmart_assistance_kiosk', type='http', auth='public', website=True)
    def kiosk(self, config_id=None, **kw):
        config = None
        employees = []
        departments = []
        if config_id:
            config = request.env['assistance.kiosk.config'].sudo().browse(int(config_id))
            employees = config.employee_ids
            departments = config.department_ids
        else:
            employees = request.env['hr.employee'].sudo().search([])
            departments = request.env['hr.department'].sudo().search([])
        # Incluye image_128 para mostrar la foto
        employees_data = [e.read(['id', 'name', 'display_name', 'pin', 'image_128'])[0] for e in employees]
        departments_data = [d.read(['id', 'name'])[0] for d in departments]
        return request.render('cleanmart_assistance_kiosk.kiosk_page', {
            'config': config,
            'employees': employees_data,
            'departments': departments_data,
        })

    @http.route('/cleanmart_assistance_kiosk/check_pin', type='json', auth='public', csrf=False)
    def check_pin(self, employee_id, pin):
        employee = request.env['hr.employee'].sudo().browse(int(employee_id))
        if employee and employee.pin == pin:
            return {'success': True}
        return {'success': False, 'error': 'PIN incorrecto'}

    @http.route('/cleanmart_assistance_kiosk/mark_attendance', type='json', auth='public', csrf=False)
    def mark_attendance(self, employee_id):
        employee = request.env['hr.employee'].sudo().browse(int(employee_id))
        if not employee:
            return {'success': False, 'error': 'Empleado no encontrado'}
        try:
            attendance = employee.sudo().attendance_action_change()
            return {
                'success': True,
                'attendance_state': attendance.get('attendance_state'),
                'action': attendance.get('action'),
                'message': attendance.get('message', ''),
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @http.route('/cleanmart_assistance_kiosk/data', type='json', auth='public', csrf=False)
    def kiosk_data(self, config_id=None):
        config = None
        employees = []
        departments = []
        if config_id:
            config = request.env['assistance.kiosk.config'].sudo().browse(int(config_id))
            employees = config.employee_ids
            departments = config.department_ids
        else:
            employees = request.env['hr.employee'].sudo().search([])
            departments = request.env['hr.department'].sudo().search([])
        employees_data = [e.read(['id', 'name', 'display_name', 'pin', 'image_128'])[0] for e in employees]
        departments_data = [d.read(['id', 'name'])[0] for d in departments]
        return {
            'employees': employees_data,
            'departments': departments_data,
        }
