from google.appengine.ext.db import djangoforms

from models import Calendar

class CalendarForm(djangoforms.ModelForm):
	class Meta:
		model = Calendar
		exclude = ['owner', 'date_added', 'date_modified']