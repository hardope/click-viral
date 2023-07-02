# Description: Views for registration
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .sendmail import send_mail
import random
from datetime import datetime, timezone

root = "/home/ubuntu/viral"
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("feed"))

    return render(request, "register.html")

def request_code(request):
    if request.method == "POST":
        username = request.POST["username"].strip()
        email = request.POST["email"].strip()

        if username == "users":
            return HttpResponse("1")

        try:
            try:
                user = User.objects.get(username=username)
                assert username == "users"
                return HttpResponse("1")
            except:
                user = User.objects.get(email=email)
                return HttpResponse("2")
        except:
            pass

        try:
            Otp.objects.get(username=username, mail=email).delete()
        except:
            pass
        otp = str(random.randint(100000, 999999))
        new_otp = Otp(username=username, mail=email, otp=otp)

        new_otp.save()
        send_mail(
            email,
            f"ClickViral OTP Verification Code For: {username}",
            f"Hello {username},\n\nYour OTP is {otp}\n\nIf You did not request this code, please ignore this email.\n\nClickViral Team",
        )
        return HttpResponse("0")


def check_otp(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        otp = request.POST["otp"]

        try:
            otp = Otp.objects.get(username=username, otp=otp, mail=email)

            if otp.tries > 10:
                return HttpResponse("2")

            created = otp.created_at
            now = datetime.now(timezone.utc)
            diff = now - created

            if diff.total_seconds() > 43200:
                return HttpResponse("2")

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            Profile(user=user).save()
            login(request, user)

            Otp.objects.get(username=username, mail=email).delete()

            return HttpResponse("0")
        except:
            try:
                otp = Otp.objects.get(username=username, mail=email)
                otp.tries += 1
                otp.save()
            except:
                pass
            return HttpResponse("1")