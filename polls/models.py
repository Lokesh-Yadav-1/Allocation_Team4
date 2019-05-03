from django.db import models


class Entry(models.Model):
	title = models.CharField(max_length=150)
	description = models.CharField(max_length=150)
	cgpa = models.IntegerField()
	count = models.IntegerField()
	# courses =  ListCharField(base_field=CharField())

class Course(models.Model):
	cid = models.ForeignKey(Entry,on_delete=models.CASCADE)
	name = models.CharField(max_length=10)