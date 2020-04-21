from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import include, path  # add include to the import apps
from . import views

app_name = "api_app"

urlpatterns = [
    path("posts/",  include('posts_app.api.api_urls'), name="posts"),
    path("auth/login/", views.Login.as_view(), name="login"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
