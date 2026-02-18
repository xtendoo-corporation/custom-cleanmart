# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class DepartmentKioskController(http.Controller):
    
    @http.route('/kiosk/department/<int:department_id>', type='http', auth='public', website=True)
    def kiosk_department(self, department_id, **kw):
        """Vista principal del kiosco por departamento"""
        _logger.info("[DEPARTMENT_KIOSK] Accessing kiosk for department ID: %s", department_id)
        
        department = request.env['hr.department'].sudo().search([
            ('id', '=', department_id),
            ('is_department_kiosk', '=', True)
        ], limit=1)
        
        if not department:
            _logger.warning("[DEPARTMENT_KIOSK] Department %s not found or not authorized", department_id)
            return request.render('cleanmart_departament_kiosk.kiosk_department_not_authorized', {
                'department_id': department_id
            })
        
        # Obtener empleados del departamento
        employees = request.env['hr.employee'].sudo().search([
            ('department_id', '=', department.id)
        ], order='name asc')
        
        employees_data = []
        for employee in employees:
            has_real_photo = bool(employee.image_1920)
            employees_data.append({
                'id': employee.id,
                'name': employee.name,
                'display_name': employee.display_name,
                'image_128': employee.image_128 if has_real_photo else False,
                'has_real_photo': has_real_photo,
                'attendance_state': employee.attendance_state,
            })
        
        return request.render('cleanmart_departament_kiosk.kiosk_department_page', {
            'department': department,
            'employees': employees_data,
        })
    
    @http.route('/kiosk/department/check_pin', type='jsonrpc', auth='public', csrf=False)
    def check_pin(self, employee_id, pin):
        """Valida el PIN del empleado"""
        _logger.info("[DEPARTMENT_KIOSK] Checking PIN for employee ID: %s", employee_id)
        
        employee = request.env['hr.employee'].sudo().browse(int(employee_id))
        
        if not employee.exists():
            return {'success': False, 'error': _('Employee not found')}
        
        if employee.pin == pin:
            _logger.info("[DEPARTMENT_KIOSK] ✓ PIN CORRECT for employee: %s", employee.name)
            return {'success': True}
        else:
            _logger.warning("[DEPARTMENT_KIOSK] ✗ INCORRECT PIN for employee: %s", employee.name)
            return {'success': False, 'error': _('Incorrect PIN')}
    
    @http.route('/kiosk/department/mark_attendance', type='jsonrpc', auth='public', csrf=False)
    def mark_attendance(self, employee_id):
        """Registra la asistencia (check in/out) del empleado"""
        _logger.info("[DEPARTMENT_KIOSK] Marking attendance for employee ID: %s", employee_id)
        
        employee = request.env['hr.employee'].sudo().browse(int(employee_id))
        
        if not employee.exists():
            return {'success': False, 'error': _('Employee not found')}
        
        try:
            employee.sudo()._attendance_action_change()
            
            action = 'check_in' if employee.attendance_state == 'checked_in' else 'check_out'
            message = _('Check In successful!') if action == 'check_in' else _('Check Out successful!')
            
            return {
                'success': True,
                'attendance_state': employee.attendance_state,
                'action': action,
                'message': message,
            }
        except Exception as e:
            _logger.error("[DEPARTMENT_KIOSK] ✗ Error marking attendance: %s", str(e))
            return {
                'success': False,
                'error': str(e)
            }
