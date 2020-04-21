from django.urls import path, include
from posts_app.api import api_views


# explanation of urlpatterns down below
urlpatterns = [
    path("", api_views.PostList.as_view(), name="post_list"),
    path("<int:pk>", api_views.PostDetail.as_view(), name="post_detail"),
]
