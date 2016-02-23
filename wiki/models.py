from __future__ import unicode_literals

from django.db import models

#from django_bleach.models import BleachField

# Create your models here.

class Tag(models.Model):
	name=models.CharField(max_length=20,primary_key=True)

class Page(models.Model):
	name=models.CharField(max_length=20,primary_key=True)
	content=models.TextField(blank=True)
	tags=models.ManyToManyField(Tag)
	#content.allowed_tags=True
	def __unicode__ (self):
		return self.content
