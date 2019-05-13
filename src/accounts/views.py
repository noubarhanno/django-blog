from django.shortcuts import render
from django.views.generic import FormView, CreateView, View
from accounts.forms import LoginForm, RegistrationForm
from PortfolioBlog.mixins import RequestFormAttachMixin,NextUrlMixin
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from accounts.models import EmailActivation
from django.urls import reverse
from .forms import RegenerateActivationForm
from django.utils.safestring import mark_safe
import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

class AccountEmailActivationView(FormMixin,View):
    success_url='login'
    form_class=RegenerateActivationForm
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key=key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirmed_qs = qs.confirmable()
            if confirmed_qs.count()==1:
                obj = confirmed_qs.first()
                obj.activate()
                messages.success(request, "your email has been activated please login", extra_tags='alert-success')
                return redirect('login')
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse('password_reset')
                    msg = """Your Email is already activated do you want
                    to <a href='{link}'>reset your password</a>
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg), extra_tags='alert-success')
                    return redirect('login')
        print(self.key)
        context = {'form' : self.get_form(), 'key': self.key}
        return render(request, 'registration/activation-error.html', context)

    def post(self,reuqest, *args, **kwargs):
        # create form to recieve an email for activation
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self,form):
        request = self.request
        msg="""Activation Link is sent , please check your email."""
        messages.success(request, msg, extra_tags='alert-success')
        email = form.cleaned_data.get('email')
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivationView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form' : form, 'key' :self.key}
        return render(self.request, 'registration/activation-error.html', context)



class LoginView(NextUrlMixin,RequestFormAttachMixin,FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    default_next='/'
    success_url='/'

    def form_valid(self, form): #form_valid is built in method should be defined
        next_url = self.get_next_url()
        return redirect(next_url) 

    def get_context_data(self, **kwargs):
        self.request.session['last_login'] = json.dumps(datetime.datetime.now(), cls=DjangoJSONEncoder)
        context = super().get_context_data(**kwargs)
        next_redirect = self.get_next_url()
        if next_redirect != '/':
            context['action_url'] = '/login/?next=%s' %(next_redirect)
        return context
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(*args, **kwargs)

# def loginView(request):
#     form = LoginForm(request.POST or None)
#     if form.is_valid():
#         username = form.cleaned_data.get("email")
#         password = form.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("/")
#         else:
#             messages.error(request, "The email or password is incorrect", extra_tags='alert-danger')
#     return render(request, "accounts/Login.html", {"form":form})

class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = "accounts/register.html"
    success_url = "/login/"

    def get_form_kwargs(self):
        kwargs = super(RegisterView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(*args, **kwargs)

    
    
