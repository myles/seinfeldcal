"""
Copyright (C) 2008 Myles Braithwaite

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from google.appengine.api import users
from google.appengine.ext import db

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect

from models import Calendar, Event
from forms import CalendarForm

def index(request):
	user = users.get_current_user()
	
	if user:
		template_name = 'calendar_list.html'
		user_calendars = db.GqlQuery("SELECT * FROM Calendar WHERE owner = :1", user)
		context = {
			'user': user,
			'calendars': user_calendars,
		}
	
	else:
		template_name = 'index.html'
		context = {}
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def calendar_add(request):
	user = users.get_current_user()
	
	if not user:
		raise Http404
	
	if request.method == 'POST':
		form = CalendarForm(data=request.POST)
		if form.is_valid():
			calendar = form.save(commit=False)
			calendar.owner = users.get_current_user()
			calendar.put()
			HttpResponseRedirect('/%s/' % calendar.slug)
	else:
		form = CalendarForm()
		return render_to_response('calendar_add.html', { 'form': form, 'user': user }, context_instance=RequestContext(request))