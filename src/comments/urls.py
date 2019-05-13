from .views import comment_thread, comment_delete, comment_update
from django.urls import path

app_name='comments'

urlpatterns =[
    path('<id>', comment_thread, name='thread'),
    path('<id>/delete-confirmation', comment_delete, name='delete'),
    path('<id>/update', comment_update, name='update')
]