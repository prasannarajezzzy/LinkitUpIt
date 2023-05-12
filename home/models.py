from django.db import models

from django.contrib.auth.models import User     #       @murthy

# makemigrations - create changes and store in a file 
# migrate - apply the pending changes created by makemigrations

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name
    
# ---------------------- my code

class JobCategory(models.Model):
    category = models.CharField(max_length=128)
    def __str__(self):
        return self.category
    
class JobStatus(models.Model):
    status = models.CharField(max_length=128)
    def __str__(self):
        return self.status
    
class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=128)
    company = models.CharField(max_length=128)
    coverLetter = models.TextField(max_length=500)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    status = models.ForeignKey(JobStatus, on_delete=models.CASCADE)
    