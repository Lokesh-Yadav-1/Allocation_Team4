from django import template
from polls.models import Entry, Course
register = template.Library()

@register.simple_tag
def index(i):
    return Entry.objects.filter(id=i)  