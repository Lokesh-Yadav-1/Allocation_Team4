from django.shortcuts import render
import requests as rq
import json

from django.http import HttpResponse
from .forms import GivePref
from polls.models import Entry, Course


def index(request):
	# need to call api to fetch available projects 
	projects = []
	titles = []
	

	headers = {'Authorization':'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI1Y2JmNzMxYzAwN2E2NTAwMTdkYzc3MDIiLCJuYW1lIjoiYXZhaXMiLCJwYXNzd29yZCI6IiQyYiQxMCRjSnp6bmw2aXNOZ1Z1QUNSSmxmUlguTWR4Y1dLZEU5UXdCclFqRGhLUXJVQWo2OXpIREhOVyIsIl9fdiI6MH0.tgt4xTy6724qLdX3l5mc1-OlN6mAEy60VVsF8hks70c','Content-Type':'application/x-www-form-urlencoded'}

	response = rq.get('https://mtech-portal.herokuapp.com/api/profentries',headers=headers)
	entry_objects = response.json()['data']

	dic_list=[]

	for p in entry_objects:
		# asked_prof_set.add(p['fid'])
		# asked_stud_count = asked_stud_count + p['count']
		entry_line ={}
		entry_line['fid']=p['fid']
		entry_line['title']=p['title']
		entry_line['desc']=p['description']
		entry_line['grade']=p['grades']
		entry_line['count']=p['count']
		entry_line['courses']=p['courses']
		dic_list.append(entry_line)

	a = dic_list

	# for i in range(0,len(a)):
	# 	projects.append(str(a[i]['title']))
	
	# if request.method == 'POST':
	# 	form = GivePref(projects,len(a),data=request.POST)
	# 	if form.is_valid():
	# 		print("yess")
	# 		prefs = {}
	# 		for each in projects:
	# 			prefs[each] = form.cleaned_data[each]
	# 		print(prefs)
	# else:
	# 	form = GivePref(projects,len(a))
			
	
	return render(request, 'student/student_application.html' , { 'entries':dic_list})

  

    



