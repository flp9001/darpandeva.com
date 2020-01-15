import datetime
from django import template

register = template.Library()



@register.filter
def next_page(page):
    try:
        return page.node.get_next_sibling().item.get_absolute_url()
    except:
        return None


@register.filter
def prev_page(page):
    try:
        return page.node.get_prev_sibling().item.get_absolute_url()
    except:
        return None
