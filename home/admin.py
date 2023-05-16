from django.contrib import admin
from home.models import Contact,JobCategory,JobStatus,Job

admin.site.register(Contact)
admin.site.register(JobCategory)
admin.site.register(JobStatus)
admin.site.register(Job)

# Register your models here.
