# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_individual_kiosk = fields.Boolean(
        string='Kiosco Individual',
        help='Marcar si este empleado tiene acceso al kiosco individual'
    )
    individual_kiosk_url = fields.Char(
        string='URL Kiosco Individual',
        compute='_compute_individual_kiosk_url',
        help='URL única para acceder al kiosco individual de este empleado'
    )

    def _compute_individual_kiosk_url(self):
        """Genera la URL única del kiosco individual para este empleado"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for employee in self:
            if employee.id:
                employee.individual_kiosk_url = f"{base_url}/kiosk/individual/{employee.id}"
            else:
                employee.individual_kiosk_url = False
