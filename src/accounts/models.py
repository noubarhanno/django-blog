from django.db import models
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from PortfolioBlog.utils import unique_key_generator
from django.template.loader import get_template
from django.conf import settings

# Create your models here.

DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS' , 7)

class MyUserManager(BaseUserManager):
    def create_user(self,name, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email or not name:
            raise ValueError("The user must specify a user name")
        user = self.model(
            name = name,
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self,name, email, password=None):
        user = self.create_user(
            name=name,
            email = email,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self,name , email, password=None):
        user = self.create_user(
            name=name,
            email=email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user
        

class MyUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    def __str__(self):
        return self.name

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['name',]

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        DEFAULT_ACTIVATION_DAYS
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        return self.filter(
            activated=False,
            forced_expired = False
        ).filter(
            timestamp__gt=start_range,
            timestamp__lte=end_range
        )

class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)
    
    def confirmable(self):
        return self.get_queryset().confirmable()
    
    def email_exists(self, email):
        return self.get_queryset().filter(
            Q(email=email)|
            Q(User__email=email)
        ).filter(
            activated=False
        )


class EmailActivation(models.Model):
    User = models.ForeignKey(MyUser , on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expired = models.IntegerField(default=7)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.User.name


    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.User
            user.is_active=True
            user.save()
            self.activated= True
            self.save()
            return True
        return False
    
    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, 'BASE_URL', 'https://www.mydomainname.com/') # the mydomainname is if the BASE_URL doesn't have value so will take the mydomainname
                key_path = reverse("account:email-activate", kwargs={'key':self.key})
                path = "{base}{path}".format(base=base_url, path=key_path)
                context = {
                    'path': path,
                    'email': self.email
                }
                txt_    = get_template("registration/emails/verify.txt").render(context)
                html_   = get_template("registration/emails/verify.html").render(context)
                subject = '1-Click Email Verification'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(
                            subject,
                            txt_,
                            from_email,
                            recipient_list,
                            html_message = html_,
                            fail_silently = False,
                )
                return sent_mail
        return False

def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)
pre_save.connect(pre_save_email_activation, sender=EmailActivation)

def post_save_user_create_receiver(sender, instance, created , *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(User=instance, email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_receiver, sender=MyUser)

    
    


