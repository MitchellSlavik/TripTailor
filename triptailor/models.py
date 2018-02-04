from django.db import models

from django.contrib.auth.models import User

class Guide(models.Model):
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		primary_key=True,
	)
	def __str__(self):
		return self.user.get_full_name()
	
class Traveler(models.Model):
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		primary_key=True,
	)
	def __str__(self):
		return self.user.get_full_name()
	
class Trip(models.Model):
	name = model.CharFeild(max_length=100)
	guide = model.ForeignKey(
		Guide,
		on_delete=models.CASCADE,
		related_name='trips',
	)
	travelers = models.ManyToManyField(
		Traveler,
		through='Ticket'
	)
	def __str__(self):
		return self.name
	
class Ticket(models.Model):
	trip = model.ForeignKey(
		Trip,
		on_delete=models.CASCADE,
	)
	traveler = model.ForeignKey(
		Traveler,
		on_delete=models.CASCADE,
	)
	num_travelers = models.IntegerField()
	
	