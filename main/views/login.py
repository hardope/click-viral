# Description: Login view
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("feed"))
    if request.method == "POST":
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        email = request.POST["email"].strip()

        try:
            user = authenticate(request, username=username, password=password)

            assert user is not None

            login(request, user)

            return HttpResponse("0")

        except:
            if email == "":
                return HttpResponse("1")

            try:
                username = User.objects.get(email__exact=email).username
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)

                    return HttpResponse("0")
                return HttpResponse("1")
            except:
                pass

            return HttpResponse("1")

    return render(request, "login.html")
