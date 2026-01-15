from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    no_visible_en_kiosco = fields.Boolean(
        string='No visible en kiosco',
        help='Si está marcado, este empleado no aparecerá en el modo quiosco de asistencias.',
        default=True
    )
