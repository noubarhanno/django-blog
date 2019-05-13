from django.urls import path
from posts.views import (
    PostCreateView, 
    PostDetailView, 
    PostListView, 
    PostDeleteView,
    PostUpdateView,
    AthorPostListView,
    ValidatePostListView,
    post_approve,
    post_hide,
)

app_name = 'posts'

urlpatterns = [
    path('create', PostCreateView.as_view(), name='create'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
    path('list', PostListView.as_view(), name='list'),
    path('validattion/list', ValidatePostListView.as_view(), name='validate_list'), 
    path('<id>/list/', AthorPostListView.as_view(), name='author_list'),
    path('<slug:slug>/delete', PostDeleteView.as_view(), name='delete'),
    path('<slug:slug>/update', PostUpdateView.as_view(), name='update'),
    path('post/<id>/approve/', post_approve, name='post_approve'),
    path('post/<id>/hide/', post_hide, name='post_hide'),
]