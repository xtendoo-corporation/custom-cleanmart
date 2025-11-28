from odoo import models, api
from .patterns import get_pattern_context, render_name_with_context


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_pattern_context(self):
        """Generate pattern context for the sale order.

        Use confirmation_date or date_order (prefer confirmation_date if confirmed),
        and partner/user language similar to invoices.
        """
        self.ensure_one()
        date = self.confirmation_date or self.date_order
        if not date:
            return {}
        lang = self.partner_id.lang or self.env.user.lang or 'en_US'
        return get_pattern_context(date, lang)

    def _replace_patterns_in_line(self, line):
        if not getattr(line, 'name', None):
            return
        context = self._get_pattern_context()
        line.name = render_name_with_context(line.name, context)

    def action_confirm(self):
        # Replace patterns on confirmation to ensure lines reflect final dates
        for order in self:
            for line in order.order_line:
                order._replace_patterns_in_line(line)
        return super().action_confirm()

    @api.model_create_multi
    def create(self, vals_list):
        # Support create with multiple value dicts
        orders = super().create(vals_list)
        # Replace patterns for each created order
        for order in orders:
            for line in order.order_line:
                order._replace_patterns_in_line(line)
        return orders
