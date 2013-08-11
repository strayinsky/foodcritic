from django.contrib.auth.models import User
from django.db import models
import datetime
from django.utils import timezone


class Restaurant(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    date = models.DateTimeField('date added')

    def __unicode__(self):
        return self.name

    def is_domestic(self):
        return self.country == "United States"


class Dish(models.Model):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=2000)
    date = models.DateTimeField('date added')

    def __unicode__(self):
        return self.name


class Grade(models.Model):
    user = models.ForeignKey(User)
    dish = models.ForeignKey(Dish)
    grade = models.PositiveIntegerField()
    date = models.DateTimeField('date added')
    comment = models.CharField(max_length=2000)


def was_graded_recently(self):
    return self.date >= timezone.now() - datetime.timedelta(days=1)
