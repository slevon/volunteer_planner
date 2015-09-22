from datetime import timedelta
from django import template
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils import timezone
from scheduler.models import Need

register = template.Library()


@register.simple_tag
def get_volunteer_number():
    return User.objects.filter(is_active=True).count()


@register.simple_tag
def get_volunteer_hours():
    """
    Returns the number of total volunteer hours worked.
    """
    finished_needs = Need.objects.filter(starting_time__lte=timezone.now())
    delta = timedelta()
    for need in finished_needs:
        delta += need.ending_time - need.starting_time
    hours = int(delta.total_seconds() / 3600)
    return intcomma(hours)
