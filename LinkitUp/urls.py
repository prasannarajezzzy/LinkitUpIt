
from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('login/', views.user_login, name="login"),
    path('pdf/', views.read_pdf, name="login"),
    path('join/', views.join, name="join"),
    path('logout/', views.user_logout, name='Logout'),
    path('jobs/', views.jobs, name='Job List'),
    path('jobs/add/', views.add, name='Add Entry'),
    path('jobs/edit/<int:id>/', views.edit, name='Edit Entry'),
    path('jobs/delete/<int:id>/', views.delete_job, name='Delete Entry'),
    path('my_view/', views.my_view, name='my_view')
]
