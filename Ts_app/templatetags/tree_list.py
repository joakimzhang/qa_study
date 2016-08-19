from django import template
register = template.Library()


def li_tree(value):
    return value.lower()

register.filter("li_tree", li_tree)