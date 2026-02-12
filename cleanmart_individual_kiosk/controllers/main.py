# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class IndividualKioskController(http.Controller):
    
    @http.route('/kiosk/individual/<int:employee_id>', type='http', auth='public', website=True)
    def kiosk_individual(self, employee_id, **kw):
        """Vista principal del kiosco individual para un empleado específico"""
        _logger.info("[INDIVIDUAL_KIOSK] Accessing kiosk for employee ID: %s", employee_id)
        
        # Buscar el empleado y validar que tenga permiso para kiosco individual
        employee = request.env['hr.employee'].sudo().search([
            ('id', '=', employee_id),
            ('is_individual_kiosk', '=', True)
        ], limit=1)
        
        if not employee:
            _logger.warning("[INDIVIDUAL_KIOSK] Employee %s not found or not authorized", employee_id)
            return request.render('cleanmart_individual_kiosk.kiosk_individual_not_authorized', {
                'employee_id': employee_id
            })
        
        # Preparar datos del empleado para el template
        # image_1920 solo existe si el usuario subió una foto real (no es el SVG autogenerado)
        has_real_photo = bool(employee.image_1920)
        
        _logger.info("[INDIVIDUAL_KIOSK] Photo detection for %s:", employee.name)
        _logger.info("[INDIVIDUAL_KIOSK]   - image_1920 exists: %s", bool(employee.image_1920))
        _logger.info("[INDIVIDUAL_KIOSK]   - image_128 exists: %s", bool(employee.image_128))
        _logger.info("[INDIVIDUAL_KIOSK]   - has_real_photo flag: %s", has_real_photo)
        
        employee_data = {
            'id': employee.id,
            'name': employee.name,
            'display_name': employee.display_name,
            'image_128': employee.image_128 if has_real_photo else False,
            'has_real_photo': has_real_photo,
            'attendance_state': employee.attendance_state,
        }
        
        _logger.info("[INDIVIDUAL_KIOSK] Employee data: has_real_photo=%s, image_128=%s", 
                     employee_data['has_real_photo'], 'SET' if employee_data['image_128'] else 'NOT_SET')
        _logger.info("[INDIVIDUAL_KIOSK] Rendering kiosk for employee: %s (state: %s)", 
                     employee.name, employee.attendance_state)
        
        return request.render('cleanmart_individual_kiosk.kiosk_individual_page', {
            'employee': employee_data,
        })
    
    @http.route('/kiosk/individual/check_pin', type='jsonrpc', auth='public', csrf=False)
    def check_pin(self, employee_id, pin):
        """Valida el PIN del empleado"""
        _logger.info("[INDIVIDUAL_KIOSK] Checking PIN for employee ID: %s", employee_id)
        _logger.info("[INDIVIDUAL_KIOSK] Received PIN: '%s' (type: %s, length: %d)", pin, type(pin).__name__, len(pin))
        
        employee = request.env['hr.employee'].sudo().browse(int(employee_id))
        
        if not employee.exists():
            _logger.error("[INDIVIDUAL_KIOSK] Employee not found: %s", employee_id)
            return {'success': False, 'error': _('Employee not found')}
        
        if not employee.is_individual_kiosk:
            _logger.error("[INDIVIDUAL_KIOSK] Employee %s not authorized for individual kiosk", employee.name)
            return {'success': False, 'error': _('Unauthorized')}
        
        _logger.info("[INDIVIDUAL_KIOSK] Expected PIN: '%s' (type: %s, length: %d)", 
                     employee.pin, type(employee.pin).__name__, len(employee.pin) if employee.pin else 0)
        
        if employee.pin == pin:
            _logger.info("[INDIVIDUAL_KIOSK] ✓ PIN CORRECT for employee: %s", employee.name)
            return {'success': True}
        else:
            _logger.warning("[INDIVIDUAL_KIOSK] ✗ INCORRECT PIN for employee: %s (expected '%s', got '%s')", 
                          employee.name, employee.pin, pin)
            return {'success': False, 'error': _('Incorrect PIN')}
    
    @http.route('/kiosk/individual/mark_attendance', type='jsonrpc', auth='public', csrf=False)
    def mark_attendance(self, employee_id):
        """Registra la asistencia (check in/out) del empleado"""
        _logger.info("[INDIVIDUAL_KIOSK] ========== MARKING ATTENDANCE ==========")
        _logger.info("[INDIVIDUAL_KIOSK] Employee ID: %s", employee_id)
        
        employee = request.env['hr.employee'].sudo().browse(int(employee_id))
        
        if not employee.exists():
            _logger.error("[INDIVIDUAL_KIOSK] Employee not found: %s", employee_id)
            return {'success': False, 'error': _('Employee not found')}
        
        if not employee.is_individual_kiosk:
            _logger.error("[INDIVIDUAL_KIOSK] Employee %s not authorized for individual kiosk", employee.name)
            return {'success': False, 'error': _('Unauthorized')}
        
        _logger.info("[INDIVIDUAL_KIOSK] Employee: %s", employee.name)
        _logger.info("[INDIVIDUAL_KIOSK] Current state BEFORE: %s", employee.attendance_state)
        
        try:
            # Realizar el cambio de asistencia
            result = employee.sudo()._attendance_action_change()
            
            _logger.info("[INDIVIDUAL_KIOSK] Current state AFTER: %s", employee.attendance_state)
            _logger.info("[INDIVIDUAL_KIOSK] _attendance_action_change result: %s", result)
            
            action = 'check_in' if employee.attendance_state == 'checked_in' else 'check_out'
            message = _('Check In successful!') if action == 'check_in' else _('Check Out successful!')
            
            _logger.info("[INDIVIDUAL_KIOSK] ✓ Attendance marked: %s for %s", action, employee.name)
            _logger.info("[INDIVIDUAL_KIOSK] ========================================")
            
            return {
                'success': True,
                'attendance_state': employee.attendance_state,
                'action': action,
                'message': message,
            }
        except Exception as e:
            _logger.error("[INDIVIDUAL_KIOSK] ✗ Error marking attendance: %s", str(e))
            _logger.exception("[INDIVIDUAL_KIOSK] Full traceback:")
            _logger.info("[INDIVIDUAL_KIOSK] ========================================")
            return {
                'success': False,
                'error': str(e)
            }
