# -*- coding: utf8 -*-
from django.db import models

class Region(models.Model):
	name = models.CharField(max_length=100)
	parent = models.ForeignKey('self', null=True, blank=True)

	def __unicode__(self):
		return self.name

class Employee(models.Model):
	user = models.ForeignKey('auth.User')
	region = models.ForeignKey(Region)
	supervisor = models.ForeignKey('self', null=True, blank=True)

	salary = models.FloatField('Salary')
	resp = models.TextField('Responsibilities', blank=True)
	skills = models.TextField('Skills', blank=True)
	pref = models.TextField('Work preferences', blank=True)

	def __unicode__(self):
		return self.user.username + ' (' + self.user.first_name + ' ' + self.user.last_name + ')'

class Shop(models.Model):
	name = models.CharField('Shop name', max_length=100)
	nip = models.CharField('Tax ID', max_length=50, blank=True)
	region = models.ForeignKey(Region)
	type = models.CharField('Shop type', max_length=1, choices=(
		('S', 'Retail shop'),
		('C', 'Food court'),
	))	
	address = models.CharField('Address', max_length=200)
	centre = models.BooleanField('Is in city centre')
	btype = models.CharField('Building type', max_length=100, blank=True)
	contact = models.TextField('Contact hints', blank=True)

	def __unicode__(self):
		return self.region.name + ': ' + self.address	

class Warehouse(models.Model):
	region = models.ForeignKey(Region)
	capacity = models.IntegerField('Capacity in kg', default=1000)
	address = models.CharField('Address', max_length=200)
	centre = models.BooleanField('Is in city centre')
	btype = models.CharField('Building type', max_length=100, blank=True)
	contact = models.TextField('Contact hints', blank=True)
	
	def __unicode__(self):
		return self.region.name + ': ' + self.address

class GoodsType(models.Model):
	name = models.CharField('Goods name', max_length=100)
	weight = models.FloatField('Weight in kg of one unit of goods', default=1)

	def __unicode__(self):
		return self.name

class Stock(models.Model):
	type = models.ForeignKey(GoodsType)
	amount = models.FloatField('Amount in goods unit')
	origin = models.ForeignKey(Warehouse, related_name='origin_warehouse', blank=True, null=True)
	def __unicode__(self):
		return self.type.name

class Sold(models.Model):
	date = models.DateTimeField()
	what = models.ForeignKey(Stock)
	amount = models.FloatField('Amount sold')
	price = models.FloatField('Order price')
	shop = models.ForeignKey(Shop)
	employee = models.ForeignKey(Employee)

	def __unicode__(self):
		return str(self.date) + ': ' + str(self.amount) + ' of ' + str(self.what.type) + ' to ' +str(self.shop.name) + ' (' + str(self.shop) + ')'


import datetime

PRIORITY_CHOICES = (
	(1, 'Low'),
	(2, 'Normal'),
	(3, 'High'),
)

class Task(models.Model):
	what = models.ForeignKey(Stock)
	amount = models.FloatField('Amount sold')
	price = models.FloatField('Order price')
	shop = models.ForeignKey(Shop)
	comment = models.CharField(max_length=250)
	created_date = models.DateTimeField(default=datetime.datetime.now)
	priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
	taskt = models.DateTimeField('Task deadline', blank=True, null=True)
	completed_date = models.DateTimeField('Completed date', blank=True, null=True)
	employee = models.ForeignKey(Employee)
	def __unicode__(self):
		return str(self.created_date)+": "+ str(self.what) + ": " + str(self.amount)+" units"
	class Meta:
		ordering = ['-priority', 'taskt']
	class Admin:
		pass
	

	
