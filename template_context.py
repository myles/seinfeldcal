from google.appengine.api import users

def google(request):
	context = {
		'login_url': users.create_login_url('/?action=login'),
		'logout_url': users.create_logout_url('/?action=logout'),
		'user': users.get_current_user(),
	}
	return context