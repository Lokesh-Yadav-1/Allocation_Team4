from flask import Flask, redirect, url_for, request 
import json
import numpy as np
import random
app = Flask(__name__) 


def stable_marriage(prof_mat,allot_count):
	a_b_mapping = {}
	a_count = []

	(n_a,n_b) = prof_mat.shape
	# i - prof
	# each - student
	track_list = []
	for i in range(n_b):
		for j in range(int(allot_count[0][i])):
			track_list.append(i)
	random.shuffle(track_list)
	# print(track_list)

	track_len = len(track_list)
	stud_count = n_a
	while (track_len != 0 and stud_count>0):
		i = track_list[0]
		# for i in track_list:
		stud_list = list(prof_mat[:,i])
		# print(stud_list)
		temp = False
		while(True):
			possible_stud = np.argwhere(stud_list == np.amax(stud_list)).flatten().tolist()
			for each in possible_stud:
				if each in a_b_mapping:
					if prof_mat[each][a_b_mapping[each]]<prof_mat[each][i]:
						# a_b_mapping.pop(each)
						# track_list.append(each)
						track_list.append(a_b_mapping[each])
						a_b_mapping[each] = i
						track_list.remove(i)
						temp = True
						break
					else:
						continue
				else:
					a_b_mapping[each] = i
					track_list.remove(i)
					temp = True
					break
			if temp:
				# print(str(i) +" -- "+ str(each))
				stud_count -= 1
				break
			else:
				for j in possible_stud:
					stud_list[j] = 0
		track_len = len(track_list)

	# print(a_b_mapping)
	# print("yaay")

	return a_b_mapping

  
@app.route('/alloc',methods = ['POST']) 
def get_alloc_data(): 
   data = request.get_data()
   # print(data)
   # print(json.loads(data))
   data = json.loads(data)
   id_A=[]
   id_B=[]
   col=0
   row=0
   rowB=0
   for features in data['A']['features']:
	  col=col+1
   for entry in data['data_A']:
	  row=row+1

   for entry in data['data_B']:
	  rowB=rowB+1
   count=0
   mat = np.zeros((row,col))
   prof_mat = np.zeros((row,rowB))
   mat.astype(float)
   prof_mat.astype(float)
   # print(data['A']['features'])


   allot_count = np.ones((1,rowB))
   allot_count.astype(int)
   for i in range(rowB):
      # print(data['data_B'][i]['fid'])
      try:
      	# print(data['final_count'][str(data['data_B'][i]['fid'])])
      	allot_count[0][i] = data['final_count'][str(data['data_B'][i]['fid'])]
      except:
  	  	continue
   print(allot_count)


   


   for features in data['A']['features']:
	  if(features['weight'] == 0 ):       #only one feature should have weight 0
		 for entry in data['data_A']:
			id_A.append(entry[features['name']])
		 count = count + 1
	  elif(features['condition'] in ["increasing", "decreasing"]):
		 col1=[]
		 maxi=0.0
		 for entry in data['data_A']:
			maxi=max(maxi,entry[features['name']])
			col1.append(float(entry[features['name']]))
		 for c in range(0,len(col1)):
			# mat[c][count] = col1[c]/maxi
			mat[c][count] = (col1[c]/maxi)*features['weight']
		 count=count+1  #used to point to the column for that feature

	  elif(features['condition'] in ("matching_without_values")):
		 #consider no grades given
		 # input is array of  key-value pair
		 for i in range(row):
			for j in range(rowB):
			   list_A =  list(data['data_A'][i]['course_taken'].keys())    #update
			   list_B = data['data_B'][j]['courses']
			   matched = list(set(list_A) & set(list_B))
			   prof_mat[i][j] += float(len(matched)*features['weight'])
		 max_val = np.amax(prof_mat) 
		 prof_mat = np.true_divide(prof_mat, max_val)
		 count=count+1  #used to point to the column for that feature
	  elif(features['condition'] in ("matching_with_values")):
		 #consider grades are given
		 # input is array of string  
		 feature_name = features['name'] 
		 mapped_feature_name = data['mapping'][feature_name]  
		 # feature_name = 'course_taken' 
		 # mapped_feature_name = 'courses'
		 for i in range(row):
			for j in range(rowB):
			   list_A =  list(data['data_A'][i][feature_name].keys())
			   list_B = data['data_B'][j][mapped_feature_name]
			   matched = list(set(list_A) & set(list_B))
			   sum_val_matched = sum([data['data_A'][i][feature_name][each] for each in matched])
			   prof_mat[i][j] += float(sum_val_matched*features['weight'])
		 max_val = np.amax(prof_mat) 
		 prof_mat = np.true_divide(prof_mat, max_val)
		 count=count+1  #used to point to the column for that feature

   # print(mat)
   # print(prof_mat)

   score_students = np.sum(mat, axis=1)
   # print(score_students)

   for i in range(prof_mat.shape[0]):
		prof_mat[i,:] = prof_mat[i,:] + score_students[i]
   # print(prof_mat)

   final_mapping = stable_marriage(prof_mat,allot_count)

#    print(final_mapping)

   final_mapping_list = []

   for k,v in final_mapping.items():
   		# print(data['data_A'][k])
   		# print(data['data_B'][v])
		final_mapping_list.append((data['data_A'][k],data['data_B'][v]))
   		# print("----------------------")
	print(json.dumps({'mapping':final_mapping_list}))
   return json.dumps({'mapping':final_mapping_list})