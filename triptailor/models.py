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
	cost = model.DecimalField(max_digits=10, decimal_places=2)
	maxNumTravelers = model.IntegerField()
	date = model.DateField()
	description = model.TextField()
	guide = model.ForeignKey(
		Guide,
		on_delete=models.CASCADE,
		related_name='trips',
	)
	travelers = models.ManyToManyField(
		Traveler,
		through='Ticket'
	)
	categories = models.ManyToManyField(
		Category,
		related_name='trips'
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
	def __str__(self):
		return self.trip.name + ' ['+self.traveler.__str__()+'] ('+num_travelers+')'
	
class Category(models.Model):
	name = model.CharFeild(max_length=100)
	isCity = model.BooleanField(default=False)
	def __str__(self):
		return self.name
	
class Location(models.Model):
	name = model.CharFeild(max_length=100)
	lat = model.DecimalField(max_digits=14, decimal_places=10)
	lng = model.DecimalField(max_digits=14, decimal_places=10)
	description = model.TextField()
	sequence = model.IntegerField()
	trip = model.ForeignKey(
		Trip,
		related_name='locaitons'
	)
	def __str__(self):
		return self.name
	
class Review:
	title = model.CharFeild(max_length=100)
	stars = model.IntegerField()
	body = model.TextField()
	traveler = model.ForeignKey(
		Traveler,
		related_name='reviews'
	)
	trip = model.ForeignKey(
		Trip,
		related_name='location'
	)
	def __str__(self):
		return self.title