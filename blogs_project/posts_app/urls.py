from django.http import HttpResponse
from django.urls import path

app_name = "posts_app"

urlpatterns = [
    path("", lambda req:HttpResponse("This is the posts page"), name="index"),
]

# For example reasons -> all urls are inside the posts_app/api folder
