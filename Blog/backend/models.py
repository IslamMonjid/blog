from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.db.models import *
from django.contrib import admin
from django.contrib.auth.models import User
import urlparse
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
import hashlib



# Create your models here.
class Blog(Model):
	title = CharField(max_length=100, unique=True)
	description = TextField()
	users = ManyToManyField(User)

	def __str__(self):
		return self.title


class Post(Model):
	user = ForeignKey(User)
	blog = ForeignKey(Blog)
	content = TextField()
	total_likes = IntegerField(null=True,blank=True, default = 0)

	def __str__(self):
		return self.content


class Comment(Model):
	user = ForeignKey(User)
	post = ForeignKey(Post)
	content = TextField()
	total_likes = IntegerField(null=True,blank=True, default = 0)

	def __str__(self):
		return self.content





