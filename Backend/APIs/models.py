from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class Department(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(max_length=300)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date_hired = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
