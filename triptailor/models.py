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

class Category(models.Model):
	name = models.CharField(max_length=100)
	isCity = models.BooleanField(default=False)
	def __str__(self):
		return self.name
	
class Trip(models.Model):
	name = models.CharField(max_length=100)
	cost = models.DecimalField(max_digits=10, decimal_places=2)
	maxNumTravelers = models.IntegerField()
	date = models.DateField()
	description = models.TextField()
	guide = models.ForeignKey(
		Guide,
		on_delete=models.CASCADE,
		related_name='trips',
	)
	travelers = models.ManyToManyField(
		Traveler,
		through='Ticket',
	)
	categories = models.ManyToManyField(
		Category,
		related_name='trips',
	)
	def __str__(self):
		return self.name
	
class Ticket(models.Model):
	trip = models.ForeignKey(
		Trip,
		on_delete=models.CASCADE,
	)
	traveler = models.ForeignKey(
		Traveler,
		on_delete=models.CASCADE,
	)
	num_travelers = models.IntegerField()
	def __str__(self):
		return self.trip.name + ' ['+self.traveler.__str__()+'] ('+self.num_travelers+')'
	
class Location(models.Model):
	name = models.CharField(max_length=100)
	lat = models.DecimalField(max_digits=14, decimal_places=10)
	lng = models.DecimalField(max_digits=14, decimal_places=10)
	description = models.TextField()
	sequence = models.IntegerField()
	trip = models.ForeignKey(
		Trip,
		related_name='locaitons',
		on_delete=models.CASCADE
	)
	def __str__(self):
		return self.name
	
class Review(models.Model):
	title = models.CharField(max_length=100)
	stars = models.IntegerField()
	body = models.TextField()
	traveler = models.ForeignKey(
		Traveler,
		related_name='reviews',
		on_delete=models.CASCADE
	)
	trip = models.ForeignKey(
		Trip,
		related_name='location',
		on_delete=models.PROTECT
	)
	def __str__(self):
		return self.title