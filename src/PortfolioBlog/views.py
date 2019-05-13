from django.contrib.auth import authenticate,login
from django.shortcuts import render , redirect
from django.contrib.auth import get_user_model

User = get_user_model()

def home_page(request):
    myUser = User.objects.filter(email=request.user.email).filter(is_admin=True)
    if myUser.exists():
        hasPower=True
    else:
        hasPower=False

    context = {
        "title": "Portofolio Blog",
        "content" : "This is my own Blog",
        "hasPower" : hasPower
    }

    if request.user.is_authenticated:
        context["premium"]="Premium"
    return render(request, "home.html", context)