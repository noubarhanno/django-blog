from django.conf.urls import include
from django.urls import path
from .views import AccountEmailActivationView

app_name='account'

urlpatterns = [
    path('email/confirm/<key>',
            AccountEmailActivationView.as_view(),
            name='email-activate'),
    path('email/resend-activation/',
            AccountEmailActivationView.as_view(),
            name='resend-activation'),
]

