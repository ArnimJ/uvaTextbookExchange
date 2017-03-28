from django import template

register = template.Library()

@register.filter(name = 'CSS', is_safe=True)
def appendCSSClass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name="toString", is_safe=True)
def toString(value):
    return str(value)

@register.simple_tag
def url_var_replace(request, variable, value):
    req = request.GET.copy()
    req[variable] = value
    return req.urlencode()

