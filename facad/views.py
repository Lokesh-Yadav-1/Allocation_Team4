from rest_framework import viewsets, filters
import os

from django.shortcuts import render
import requests as rq
import json
# Create your views here.
from django.http import HttpResponse

from polls.forms import AddEntryForm
from facad.forms import weightForm

from django.contrib.staticfiles.templatetags.staticfiles import static

from mysite.settings import BASE_DIR


def index(request):
	headers = {'Authorization':'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI1Y2JmNzMxYzAwN2E2NTAwMTdkYzc3MDIiLCJuYW1lIjoiYXZhaXMiLCJwYXNzd29yZCI6IiQyYiQxMCRjSnp6bmw2aXNOZ1Z1QUNSSmxmUlguTWR4Y1dLZEU5UXdCclFqRGhLUXJVQWo2OXpIREhOVyIsIl9fdiI6MH0.tgt4xTy6724qLdX3l5mc1-OlN6mAEy60VVsF8hks70c','Content-Type':'application/x-www-form-urlencoded'}
	
	response = rq.get('https://mtech-portal.herokuapp.com/api/students',headers=headers)
	stud_data = response.json()['data']
	
	response = rq.get('https://mtech-portal.herokuapp.com/api/faculties',headers=headers)
	prof_data = response.json()['data']

	response = rq.get('https://mtech-portal.herokuapp.com/api/studentsubjects',headers=headers)
	subj_data = response.json()['data']

	response = rq.get('https://mtech-portal.herokuapp.com/api/profentries',headers=headers)
	entries_data = response.json()['data']

	# print(entries_data)
	dic_list = []
	
	prof_set = set()
	asked_prof_set = set()
	asked_stud_count =0
	asked_prof_count=0
	total_prof=0
	total_stud=0
	for p in prof_data:
		prof_set.add(p['fid'])

	total_prof = len(prof_set)

	for p in entries_data:
		asked_prof_set.add(p['fid'])
		asked_stud_count = asked_stud_count + p['count']
		entry_line ={}
		entry_line['fid']=p['fid']
		entry_line['title']=p['title']
		entry_line['desc']=p['description']
		entry_line['grade']=p['grades']
		entry_line['count']=p['count']
		entry_line['courses']=p['courses']
		dic_list.append(entry_line)

	# print(prof_set)
	asked_prof_count = len(asked_prof_set)

	for p in stud_data:
		total_stud = total_stud + 1
	
	count_dict={}    # to count total number of students required by each prof

	for p in entries_data:
		if str(p['fid']) in count_dict:
			count_dict[str(p['fid'])]=count_dict[str(p['fid'])] + p['count']
		else:
			count_dict[str(p['fid'])]=p['count']

	course_mapping = {}

	grade_mapping = {'AA':10,'AB':9,'BB':8,'BC':7,'CC':6,'CD':5}

	for each in subj_data:
		rn = each['RollNo']
		if each['GradeID'] in grade_mapping:
			grade = grade_mapping[each['GradeID']]
		else:
			grade = 0
		if rn in course_mapping:
			course_mapping[rn][each['Topic']] = grade
		else:
			course_mapping[rn] = {each['Topic']:grade}

	# print(stud_data)

	for each in stud_data:
		rn = each['RollNo']
		each['course_taken'] = course_mapping[rn]

	# print(stud_data)

	# data_alloc = {'stud' : stud_data, 'prof':prof_data}

	json_data = os.path.join(BASE_DIR, 'static','json')
	data_try = json.load(open(json_data))

	data_try["data_A"] = stud_data
	data_try["data_B"] = prof_data

	fac_count = {"1000":2}
	data_try["final_count"] = count_dict


	map_list=[]
	ui_list=[]
	if request.method == 'POST' and 'btnalloc' in request.POST:
		form = weightForm(data=request.POST)
		if form.is_valid():
			cgpa_weight = form.cleaned_data['cgpa_weight']
			courses_weight = form.cleaned_data['courses_weight']

			if form.cleaned_data['cgpa_weight'] is None:
				cgpa_weight = 0.9
			if form.cleaned_data['courses_weight'] is None:
				courses_weight = 0.9

			data_try['A']['features'][2]['weight'] = cgpa_weight
			data_try['A']['features'][4]['weight'] = courses_weight

			local_response = rq.post('http://localhost:5000/alloc',data=json.dumps(data_try))
			map_list=local_response.json()['mapping']

			for i in  map_list:
				# print(i[0])
				ui_dict={}
				ui_dict['sname']=i[0]['firstName']+" "+i[0]['lastName']
				ui_dict['pname']= i[1]['firstName']+" "+i[1]['lastName']
				# print(ui_dict)
				ui_list.append(ui_dict)

	else:
		form = weightForm()

	

	# flask_response = rq.post('http://10.130.171.233:5000/alloc',data=json.dumps(data_alloc))
	# print(flask_response)

	return render(request, 'facad/main.html', {'ui_list':ui_list ,'form':form, 'asked_prof_count': asked_prof_count, 'asked_stud_count': asked_stud_count, 'total_prof':total_prof, 'total_stud':total_stud,'entries': dic_list})
