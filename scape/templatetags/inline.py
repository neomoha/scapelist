# -*- coding: utf-8 -*-

# This file is part of ScapeList.
#
# ScapeList is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ScapeList is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ScapeList.  If not, see <http://www.gnu.org/licenses/>.

# Written by Mohamed Sordo (@neomoha)
# Email: mohamed ^dot^ sordo ^at^ gmail ^dot^ com
# Website: http://msordo.weebly.com

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