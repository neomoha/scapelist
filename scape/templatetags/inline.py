from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

from django.utils.http import urlquote, urlquote_plus

register = template.Library()

### SOCIAL PART ###
@register.simple_tag
def inline_user(user):
    if len(user.first_name) == 0:
        return '<a href="%s">%s</a>' % (reverse('social-user-page', args=[user.username]), user.username)
    else:
        return '<a href="%s">%s %s</a>' % (reverse('social-user-page', args=[user.username]), user.first_name, user.last_name)