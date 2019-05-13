from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from posts.models import Posts
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from activities.models import Activity
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.

User = get_user_model()

class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    likes = GenericRelation(Activity, related_query_name='comments')
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    # def approve(self):
    #     self.approved_comment=True
    #     self.save()

    def get_absolute_url(self):
        return reverse("comments:thread", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"id": self.id})
    
    def get_update_url(self):
        return reverse("comments:update", kwargs={"id": self.id})
    
    def children(self): #replies
        return Comment.objects.filter(parent=self)
    
    @property
    def is_child(self):
        if not self.parent:
            return False
        return True

    def is_parent(self):
        if not self.parent:
            return True
        return False

