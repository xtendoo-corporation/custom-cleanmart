from odoo import models
from .patterns import get_pattern_context, render_name_with_context


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_pattern_context(self):
        """Wrapper that returns the pattern context for this move.

        Prefer invoice_date over date. Use partner lang or user lang as fallback.
        """
        self.ensure_one()
        date = self.invoice_date or self.date
        if not date:
            return {}
        lang = self.partner_id.lang or self.env.user.lang or 'en_US'
        return get_pattern_context(date, lang)

    def _replace_patterns_in_line(self, line):
        """Replace patterns in the line's name using the pattern context."""
        if not getattr(line, 'name', None):
            return
        context = self._get_pattern_context()
        line.name = render_name_with_context(line.name, context)

    def action_post(self):
        """Override action_post to replace patterns in invoice lines before posting."""
        for move in self:
            if move.move_type in ['out_invoice', 'out_refund']:
                for line in move.invoice_line_ids:
                    move._replace_patterns_in_line(line)
        return super().action_post()
