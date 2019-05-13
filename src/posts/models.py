from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import MyUser
from django.db.models.signals import pre_save
from PortfolioBlog.utils import unique_slug_generator, get_read_time
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericRelation
from activities.models import Activity
from tinymce import HTMLField


User = get_user_model()

# Create your models here.

def upload_location(instance, filename):
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    return "%s/%s" %(new_id, filename)

class PostsQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(status='D')
    def search(self,query):
        lookups = Q(title__icontains=query)| Q(content__icontains=query)
        #Q(tag__name__icontains=query)
        return self.filter(lookups).filter(status='P').distinct()
    def search_author(self,query):
        lookups = Q(user__iexact=query)
        return self.filter(lookups).filter(status='P').distinct()

class PostsModelManager(models.Manager):
    def get_queryset(self):
        return PostsQuerySet(self.model, using=self._db)
    def search(self, query):
        return self.get_queryset().active().search(query)
    def validate_posts(self):
        return self.get_queryset().filter(status='D').filter(validate=True)

class Posts(models.Model):
    DRAFT = 'D'
    HIDDEN = 'H'
    PUBLISHED = 'P'
    ENTRY_STATUS = (
        (DRAFT, 'Draft'),
        (HIDDEN, 'Hidden'),
        (PUBLISHED, 'Published'),
    )
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    slug        = models.SlugField(max_length=255 ,blank=True, unique=True)
    title       = models.CharField(max_length=120, blank=True, null=True)
    content     = HTMLField('content')
    status      = models.CharField(max_length=10, choices=ENTRY_STATUS, default=DRAFT)
    validate    = models.BooleanField(default=False)
    activities  = GenericRelation(Activity, related_query_name='posts')
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    read_time   = models.IntegerField(default=0)
    image       = models.ImageField(upload_to=upload_location, blank=True, null=True)

    objects = PostsModelManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created", "-updated"]

    def approve(self):
        self.status='P'
        self.save()

    def hide(self):
        self.status='H'
        self.save()
    
    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})
    
    def approved_comments(self):
        return self.comments.filter(approved_comment=True).filter(parent=None)

    def get_likes(self):
        return self.activities.filter(activity_type=Activity.LIKE)

    def get_posts(self):
        return reverse("posts:author_list", kwargs={"id": self.user.id})




def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var

pre_save.connect(pre_save_post_receiver , sender=Posts)



    


    

    

    
