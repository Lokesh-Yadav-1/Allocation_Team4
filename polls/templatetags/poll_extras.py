from django import template
from polls.models import Entry, Course

register = template.Library()

@register.simple_tag
def get_course(entry_id):
	answers = Course.objects.filter(cid_id=entry_id)
	return answers