from google.appengine.api import users
from django.conf import settings

def google(request):
	context = {
		'login_url': users.create_login_url('/?action=login'),
		'logout_url': users.create_logout_url('/?action=logout'),
		'user': users.get_current_user(),
	}
	return context

def media(request):
	context = {
		'MEDIA_URL': settings.MEDIA_URL,
	}
	return context
