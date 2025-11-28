from odoo import models, api
from .patterns import get_pattern_context, render_name_with_context
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_pattern_context(self):
        """Generate pattern context for the sale order.

        Use confirmation_date or date_order (prefer confirmation_date if confirmed),
        and partner/user language similar to invoices. This method is defensive and
        will return an empty context instead of raising if required fields are missing.
        """
        try:
            self.ensure_one()
            # Check field presence in model fields to avoid AttributeError
            if 'confirmation_date' in getattr(self, '_fields', {}):
                confirmation_date = getattr(self, 'confirmation_date', False)
            else:
                confirmation_date = False
            date = confirmation_date or getattr(self, 'date_order', False)
            if not date:
                return {}
            lang = (self.partner_id.lang if getattr(self, 'partner_id', False) and self.partner_id else None) or self.env.user.lang or 'en_US'
            return get_pattern_context(date, lang)
        except AttributeError as e:
            # Defensive: if some attribute is missing on the record, return empty context
            _logger.debug('Missing attribute when building pattern context for sale.order: %s', e)
            return {}
        except Exception:
            # Avoid letting unexpected exceptions break create/web_save flow; log and return empty context
            _logger.exception('Error computing pattern context for sale.order')
            return {}

    def _replace_patterns_in_line(self, line):
        if not getattr(line, 'name', None):
            return
        try:
            context = self._get_pattern_context()
            if context:
                line.name = render_name_with_context(line.name, context)
        except Exception:
            # Log debug and continue; don't raise during web requests or demo load
            _logger.exception('Failed to replace patterns in sale.order line %s', getattr(line, 'id', 'n/a'))
            return

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
