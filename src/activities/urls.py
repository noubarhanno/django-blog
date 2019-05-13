from .views import PostLike, PostLikes
from django.urls import path

app_name='activities'

urlpatterns =[
    path('like/', PostLike.as_view(), name='like'),
    path('likes/count/',PostLikes.as_view(), name='likes_count')
]