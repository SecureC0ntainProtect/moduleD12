from django import template


register = template.Library()

censor_word = [
    'нецензурное слово',
]


@register.filter(name='censor')
def censor(value, _):
    for word in censor_word:
        value = str(value).replace(word, '*****')
    return str(value)
