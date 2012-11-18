from django.conf import settings
from django import template
import datetime
import pytz

import logging
logger = logging.getLogger(__name__)

register = template.Library()

def pluralize(s,num):
	if num > 1:
		return s + 's'
	return s

@register.filter
def smarttime(dt):
	now = datetime.datetime.utcnow()
	#logger.debug('Now,dt ' + str(now) + ' ' + str(dt))
	diff = now - dt
	#logger.debug(str(diff) + ' %i days, %i hours, %i minutes, %i seconds' % (diff.days, diff.seconds/3600, diff.seconds/60, diff.seconds))
	if diff.days < 7:
		if diff.days < 1:
			minutes = diff.seconds/60
			if diff.days < 0:
				minutes += diff.days * 24 * 60
			if minutes <= 0:
				return '0 minutes ago'
			elif minutes < 60:
				return '%i %s ago' % (minutes, pluralize('minute',minutes))
			else:
				return '%i %s ago' % ((minutes/60), pluralize('hour',minutes/60))
		else:
			return '%i %s ago' % (diff.days, pluralize('day', diff.days))
	else:
		# Convert time to current time zone
		tz = pytz.timezone(settings.TIME_ZONE)
		dt = dt.replace(tzinfo=pytz.utc)
		return dt.astimezone(tz).strftime('%b %d, %Y').replace(' 0', ' ')