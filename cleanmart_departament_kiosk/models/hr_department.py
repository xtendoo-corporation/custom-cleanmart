# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    is_department_kiosk = fields.Boolean(
        string='Kiosco de Departamento',
        help='Marcar si este departamento tiene acceso al kiosco de departamento'
    )
    department_kiosk_url = fields.Char(
        string='URL Kiosco de Departamento',
        compute='_compute_department_kiosk_url',
        help='URL única para acceder al kiosco de este departamento'
    )

    def _compute_department_kiosk_url(self):
        """Genera la URL única del kiosco para este departamento"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for department in self:
            if department.id:
                department.department_kiosk_url = f"{base_url}/kiosk/department/{department.id}"
            else:
                department.department_kiosk_url = False
