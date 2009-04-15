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

import datetime, time

from google.appengine.api import users
from google.appengine.ext import db

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect, HttpResponse

from models import Event

def index(request, year=str(datetime.date.today().year), month=datetime.date.today().strftime('%b').lower()):
	user = users.get_current_user()
	
	if user:
		template_name = 'calendar.html'
		
		try:
			month = datetime.date(*time.strptime(year+month, '%Y%b')[:3])
		except ValueError:
			raise Http404
		
		if month == datetime.date.today():
			today = True
		else:
			today = False
		
		first_day = month.replace(day=1)
		if first_day.month == 12:
			last_day = first_day.replace(year=first_day.year + 1, month=1)
		else:
			last_day = first_day.replace(month=first_day.month + 1)
		
		# event_list = db.GqlQuery("SELECT * FROM Event WHERE owner = :user AND date >= :start_date AND date <= :end_date", user=user, start_date=first_day, end_date=last_day)
		
		first_weekday = first_day - datetime.timedelta(first_day.weekday())
		last_weekday = last_day + datetime.timedelta(7 - last_day.weekday())
		
		month_cal = []
		week = []
		week_headers = []

		i = 0
		day = first_weekday
		while day <= last_weekday:
			if i < 7:
				week_headers.append(day)
			cal_day = {}
			cal_day['day'] = day
			cal_day['events'] = db.GqlQuery("SELECT * FROM Event WHERE owner = :user AND date = :date", user=user, date=day).fetch(1)
			if day.month == month.month:
				cal_day['in_month'] = True
			else:
				cal_day['in_month'] = False
			if day == datetime.date.today():
				cal_day['today'] = True
			else:
				cal_day['today'] = False
			if day.weekday() == 6 or day.weekday() == 5:
				cal_day['weekend'] = True
			else:
				cal_day['weekend'] = False
			week.append(cal_day)
			if day.weekday() == 6:
				month_cal.append(week)
				week = []
			i += 1
			day += datetime.timedelta(1)
		
		context = {
			'calendar': month_cal,
			'headers': week_headers,
			'month': month,
		}
	else:
		template_name = 'index.html'
		context = {}
	
	return render_to_response(template_name, context, context_instance=RequestContext(request))

def add(request):
	user = users.get_current_user()
	
	if request.POST and user:
		post_date = request.POST.get('date', False)
		date = datetime.date(*time.strptime(post_date, '%Y-%m-%d')[:3])
		event = Event(date=date, owner=user)
		event.put()
		return HttpResponse("Successed at marking the date %s." % date)
	
	return HttpResponse("Failure.")