from odoo import models, fields, api

class HrDepartment(models.Model):
    _inherit = 'hr.department'

    hide_departament_in_kiosk = fields.Boolean(
        string='Ocultar en modo quiosco',
        help='Si está marcado, este departamento no aparecerá en el modo quiosco de asistencias.'
    )

    @api.model
    def get_departments_for_kiosk(self, company_id):
        return self.sudo().search([
            ('company_id', '=', company_id),
            ('hide_departament_in_kiosk', '=', False)
        ])
