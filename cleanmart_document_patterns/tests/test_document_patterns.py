from odoo.tests.common import TransactionCase
from datetime import date


class TestDocumentPatterns(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'lang': 'es_ES',
        })
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'service',
        })

    def test_invoice_patterns_replacement(self):
        move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'invoice_date': date(2025, 11, 15),
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 100.0,
                'name': 'Servicios de limpieza {{month_and_year}}'
            })]
        })
        # Post the invoice which should trigger replacement
        move.action_post()
        self.assertIn('noviembre 2025', move.invoice_line_ids[0].name)

    def test_invoice_previous_month_edge(self):
        move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'invoice_date': date(2025, 1, 5),
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 50.0,
                'name': 'Periodo anterior {{previous_month_and_year}}'
            })]
        })
        move.action_post()
        # previous month of Jan 2025 is Dec 2024
        self.assertIn('diciembre 2024', move.invoice_line_ids[0].name)

    def test_sale_order_quote_replacement_on_create(self):
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'date_order': date(2025, 11, 15),
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'price_unit': 10.0,
                'name': 'Mantenimiento servidores {{month}} {{year}}'
            })]
        })
        # On create we replace in this implementation
        self.assertIn('noviembre', order.order_line[0].name)
        self.assertIn('2025', order.order_line[0].name)

    def test_sale_order_confirm_replacement(self):
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'date_order': date(2025, 10, 10),
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 2,
                'price_unit': 20.0,
                'name': 'Servicios {{month_and_year}}'
            })]
        })
        order.action_confirm()
        self.assertIn('octubre 2025', order.order_line[0].name)

