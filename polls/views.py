from rest_framework import viewsets, filters
import os

from django.shortcuts import render
import requests as rq
import json
# Create your views here.
from django.http import HttpResponse

from polls.forms import AddEntryForm
from .models import Entry, Course

from django.contrib.staticfiles.templatetags.staticfiles import static

from mysite.settings import BASE_DIR

cou = []

def index(request):

	# entry_objects= Entry.objects.all()
	# course_objects= Course.objects.all()

	

	headers = {'Authorization':'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI1Y2JmNzMxYzAwN2E2NTAwMTdkYzc3MDIiLCJuYW1lIjoiYXZhaXMiLCJwYXNzd29yZCI6IiQyYiQxMCRjSnp6bmw2aXNOZ1Z1QUNSSmxmUlguTWR4Y1dLZEU5UXdCclFqRGhLUXJVQWo2OXpIREhOVyIsIl9fdiI6MH0.tgt4xTy6724qLdX3l5mc1-OlN6mAEy60VVsF8hks70c','Content-Type':'application/x-www-form-urlencoded'}

	response = rq.get('https://mtech-portal.herokuapp.com/api/profentries',headers=headers).json()['data']
	next_id = len(response) + 1

	response = rq.get('https://mtech-portal.herokuapp.com/api/studentsubjects',headers=headers)
	subj_data = response.json()['data']

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


	subj_list = []
	for each in subj_data:
		subj_list.append(each['Topic'])
	print("Subject")
	subj_list = list(set(subj_list))

	if request.method == 'POST' and 'btnform1' in request.POST:
		form = AddEntryForm(data=request.POST,tup=subj_list)

		if form.is_valid():
			fid = form.cleaned_data['fid']
			title_data = form.cleaned_data['title']
			description_data = form.cleaned_data['description']
			cgpa_data = form.cleaned_data['cgpa']
			count_data = form.cleaned_data['count']
			print("Entry: "+str(fid)+ " "+title_data + " " + description_data + " " + str(cgpa_data) + " " + str(count_data) + " "+str(cou))

			json_obj = {"id":next_id,"fid":fid,"grades":cgpa_data,"count":count_data,"courses":cou}

			print(json_obj)

			r = rq.post('https://mtech-portal.herokuapp.com/api/profentries',headers=headers, data=json_obj)
			# print("done "+str(r))

			# payload = {"id":8}
			# url = "https://mtech-portal.herokuapp.com/api/profentries"
			# r = rq.delete(url, data=payload, headers=headers)
			# print("done "+str(r))

			# c = Entry.objects.all().count()

			# obj = Entry()
			# obj.title = title_data
			# obj.description = description_data
			# obj.cgpa = cgpa_data
			# obj.count = count_data
			# obj.save()

			# for i in range(len(cou)):		
			# 	obj_c = Course()
			# 	obj_c.cid = obj
			# 	obj_c.name = cou[i]
			# 	obj_c.save()

			form = AddEntryForm(subj_list)
		else:
			form = AddEntryForm(data=request.POST,tup=subj_list)


	elif request.method=='POST' and 'btnform2' in request.POST:
		form = AddEntryForm(data=request.POST,tup=subj_list)
		if form.is_valid():
			x = form.cleaned_data['courses']
			print(x)
			cou.append(x)
	else:
		form = AddEntryForm(subj_list)

	geodata = {'Hello':'World'}




	return render(request, 'polls/index.html', {'form': form ,'data':geodata, 'entries':dic_list})

