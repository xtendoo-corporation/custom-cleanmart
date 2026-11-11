from odoo.tests import tagged
from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestInvoiceReceipt(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.partner_a
        cls.bank = cls.env["res.partner.bank"].sudo().create(
            {"acc_number": "ES5420980276590132003530", "partner_id": cls.partner.id}
        )
        cls.invoice = cls.init_invoice(
            "out_invoice", partner=cls.partner, amounts=[865.53], post=True
        )
        cls.invoice.partner_bank_id = cls.bank

    def _html(self, xmlid):
        html, _ = self.env["ir.actions.report"]._render_qweb_html(
            xmlid, self.invoice.ids
        )
        return html.decode()

    def test_receipt_report_contains_receipt(self):
        html = self._html("cleanmart_document_format.report_invoice_with_receipt")
        self.assertIn("o_cleanmart_receipt", html)
        self.assertIn("2098 0276 59 0132003530", html)
        self.assertIn("Recibo bancario", html)

    def test_standard_report_has_no_receipt(self):
        html = self._html("account.report_invoice_with_payments")
        self.assertNotIn("o_cleanmart_receipt", html)
