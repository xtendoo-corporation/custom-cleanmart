# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import logging

_logger = logging.getLogger(__name__)


class CustomerPortalAttendance(CustomerPortal):
    
    @http.route(['/my/attendance', '/my/attendance/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_attendance(self, page=1, **kw):
        """Página principal de asistencias del empleado"""
        _logger.info("[ATTENDANCE] ==================== START ====================")
        _logger.info("[ATTENDANCE] Accessing /my/attendance route")
        _logger.info("[ATTENDANCE] Current user: %s (ID: %s)", request.env.user.name, request.env.user.id)

        user = request.env.user
        employee = user.employee_id
        
        if not employee:
            return request.render('cleanmart_portal_assistance.portal_attendance_no_employee')
        
        # Obtener datos del empleado
        values = self._prepare_portal_layout_values()
        values.update({
            'employee': employee,
            'attendance_state': employee.attendance_state,
            'hours_today': employee.hours_today,
            'hours_previously_today': employee.hours_previously_today,
            'last_attendance_worked_hours': employee.last_attendance_worked_hours,
            'last_check_in': employee.last_check_in,
            'last_check_out': employee.last_check_out,
            'total_overtime': employee.total_overtime,
            'display_overtime': employee.company_id.hr_attendance_display_overtime,
            'page_name': 'attendance',
        })
        
        return request.render('cleanmart_portal_assistance.portal_my_attendance', values)
    
    @http.route(['/my/attendance/action'], type='json', auth='user')
    def portal_attendance_action(self, **kw):
        """Endpoint para realizar check in/out"""
        try:
            user = request.env.user
            employee = user.employee_id
            
            if not employee:
                return {
                    'success': False,
                    'error': _('No employee found for this user')
                }
            
            # Realizar el cambio de asistencia
            attendance = employee._attendance_action_change()
            
            # Refrescar datos del empleado
            employee.invalidate_recordset()
            
            return {
                'success': True,
                'attendance_state': employee.attendance_state,
                'hours_today': round(employee.hours_today, 2),
                'hours_previously_today': round(employee.hours_previously_today, 2),
                'last_attendance_worked_hours': round(employee.last_attendance_worked_hours, 2),
                'last_check_in': employee.last_check_in.strftime('%H:%M:%S') if employee.last_check_in else '',
                'last_check_out': employee.last_check_out.strftime('%H:%M:%S') if employee.last_check_out else '',
                'message': _('Check In successful!') if employee.attendance_state == 'checked_in' else _('Check Out successful!'),
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @http.route(['/my/attendance/history'], type='http', auth='user', website=True)
    def portal_attendance_history(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        """Historial de asistencias del empleado"""
        
        # Obtener el empleado del usuario actual
        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', request.env.user.id)
        ], limit=1)
        
        _logger.info("[ATTENDANCE] Employee search result: %s", employee)
        if employee:
            _logger.info("[ATTENDANCE] Employee found: %s (ID: %s)", employee.name, employee.id)
        else:
            _logger.warning("[ATTENDANCE] No employee found for user %s", request.env.user.name)
        
        if not employee:
            _logger.info("[ATTENDANCE] Rendering no_employee template")
            return request.render('cleanmart_portal_assistance.portal_attendance_no_employee', {})

        
        # Configurar búsqueda y paginación
        Attendance = request.env['hr.attendance']
        domain = [('employee_id', '=', employee.id)]
        
        # Filtros de fecha
        if date_begin:
            domain.append(('check_in', '>=', date_begin))
        if date_end:
            domain.append(('check_in', '<=', date_end))
        
        # Ordenamiento
        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'check_in desc'},
            'hours': {'label': _('Hours'), 'order': 'worked_hours desc'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        
        # Paginación
        attendances_per_page = 20
        attendance_count = Attendance.search_count(domain)
        pager = request.website.pager(
            url='/my/attendance/history',
            total=attendance_count,
            page=page,
            step=attendances_per_page,
            url_args={'sortby': sortby},
        )
        
        attendances = Attendance.search(
            domain,
            order=order,
            limit=attendances_per_page,
            offset=pager['offset']
        )
        
        values = self._prepare_portal_layout_values()
        values.update({
            'employee': employee,
            'attendances': attendances,
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'page_name': 'attendance_history',
        })
        
        return request.render('cleanmart_portal_assistance.portal_attendance_history', values)
