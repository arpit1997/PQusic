from django.db import models
from django.contrib.auth.models import User


class AppUser(models.Model):
	"""
	extended user model for application user
	"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# True is for public user
	privacy = models.BooleanField(default=True)
