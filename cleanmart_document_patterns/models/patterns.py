# -*- coding: utf-8 -*-
from odoo import _
from babel import Locale
import calendar
from dateutil.relativedelta import relativedelta


def get_pattern_context(date, lang):
    """Return a dict with pattern values based on date and lang.

    Expected keys: month, year, month_and_year, previous_month_and_year.
    `date` can be a date or datetime.
    """
    # Normalize
    if not date:
        return {}
    try:
        month = date.month
        year = date.year
    except Exception:
        return {}

    prev = date - relativedelta(months=1)
    prev_month = prev.month
    prev_year = prev.year

    # Resolve locale month names
    if lang:
        try:
            locale = Locale.parse(lang)
            month_name = locale.months['format']['wide'][month]
            prev_month_name = locale.months['format']['wide'][prev_month]
        except Exception:
            month_name = calendar.month_name[month]
            prev_month_name = calendar.month_name[prev_month]
    else:
        month_name = calendar.month_name[month]
        prev_month_name = calendar.month_name[prev_month]

    return {
        'month': month_name,
        'year': str(year),
        'month_and_year': f"{month_name} {year}",
        'previous_month_and_year': f"{prev_month_name} {prev_year}",
    }


def render_name_with_context(name, context):
    """Render the given name replacing {{key}} with context values.

    This function will only replace known keys to avoid accidental substitution.
    It supports patterns like {{month}} and {{year}}.
    """
    if not name or not context:
        return name
    # Simple replacement to avoid templating engine complexity
    result = name
    for key, val in context.items():
        result = result.replace('{{' + key + '}}', val)
    return result

