from google.appengine.ext.db import djangoforms

from models import Event

class EventForm(djangoforms.ModelForm):
	class Meta:
		model = Event
		exclude = ['owner', 'date_added', 'date_modified']