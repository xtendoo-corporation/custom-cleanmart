from odoo.addons.hr_attendance.controllers.main import HrAttendance
from odoo.http import request, route
from odoo.fields import Domain
from odoo.tools.image import image_data_uri

class HrAttendanceKioskCustom(HrAttendance):
    @route(["/hr_attendance/<token>"], type='http', auth='public', website=True, sitemap=True)
    def open_kiosk_mode(self, token, from_trial_mode=False):
        company = self._get_company(token)
        if not company:
            return request.not_found()
        else:
            department_list = [
                {"id": dep.id, "name": dep.name, "count": dep.total_employee}
                for dep in request.env["hr.department"]
                .with_context(allowed_company_ids=[company.id])
                .sudo()
                .search([
                    ("company_id", "=", company.id),
                    ("hide_departament_in_kiosk", "=", False)
                ])
                if dep.name and dep.name.lower() != "all"
            ]
            has_password = self.has_password()
            if not from_trial_mode and has_password:
                request.session.logout(keep_db=True)
            if (from_trial_mode or (not has_password and not request.env.user.is_public)):
                kiosk_mode = "settings"
            else:
                kiosk_mode = company.attendance_kiosk_mode
            from odoo.service.common import exp_version
            from odoo.tools import py_to_js_locale
            version_info = exp_version()
            return request.render(
                'hr_attendance.public_kiosk_mode',
                {
                    'kiosk_backend_info': {
                        'token': token,
                        'company_id': company.id,
                        'company_name': company.name,
                        'departments': department_list,
                        'kiosk_mode': kiosk_mode,
                        'from_trial_mode': from_trial_mode,
                        'barcode_source': company.attendance_barcode_source,
                        'device_tracking_enabled': company.attendance_device_tracking,
                        'lang': py_to_js_locale(company.partner_id.lang or company.env.lang),
                        'server_version_info': version_info.get('server_version_info'),
                    },
                }
            )
        return super().open_kiosk_mode(token, from_trial_mode)

    @route('/hr_attendance/employees_infos', type="jsonrpc", auth="public")
    def employees_infos(self, token, limit, offset, domain):
        company = self._get_company(token)
        if company:
            domain = Domain(domain) & Domain('company_id', '=', company.id) & Domain('no_visible_en_kiosco', '=', False)
            employees = request.env['hr.employee'].sudo().search_fetch(domain, ['id', 'display_name', 'job_id'],
                limit=limit, offset=offset, order="name, id")
            employees_data = [{
                'id': employee.id,
                'display_name': employee.display_name,
                'job_id': employee.job_id.name,
                'avatar': image_data_uri(employee.avatar_128),
                'status': employee.attendance_state,
                'mode': employee.last_attendance_id.in_mode
            } for employee in employees]
            return {'records': employees_data, 'length': request.env['hr.employee'].sudo().search_count(domain)}
        return []
