from odoo import models, fields

class AssistanceKioskConfig(models.Model):
    _name = 'assistance.kiosk.config'
    _description = 'Configuración de Kiosko de Asistencias Cleanmart'

    name = fields.Char('Nombre', required=True)
    department_ids = fields.Many2many('hr.department', string='Departamentos permitidos')
    employee_ids = fields.Many2many('hr.employee', string='Empleados permitidos')
    active = fields.Boolean('Activo', default=True)
