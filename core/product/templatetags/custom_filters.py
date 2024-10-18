# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})


@register.filter(name='add_label_class')
def add_label_class(value, css_class):
    return value.label_tag(attrs={'class': css_class})
