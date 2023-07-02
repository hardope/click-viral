# Desc: Views for the security page
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Otp
from .sendmail import send_mail
from datetime import datetime, timezone
import random

def security(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    if request.method == "POST":
        if request.POST.get("action") == "change_username":
            username = request.POST.get("username").strip()
            if request.user.username == username:
                return JsonResponse({"response": "Username is the same as before"})
            if User.objects.filter(username=username).exists():
                return JsonResponse({"response": "Username already exists"})
            else:
                request.user.username = username
                request.user.save()
                return JsonResponse({"response": "Username changed successfully"})
        elif request.POST.get("action") == "change_password":
            password = request.POST.get("password")
            confirm = request.POST.get("confirm_password")
            if request.user.check_password(password):
                return JsonResponse({"response": "Password is the same as before"})
            if password != confirm:
                return JsonResponse(
                    {"response": "Password and confirmation does not match"}
                )
            else:
                username = request.user.username
                request.user.set_password(password)
                request.user.save()
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return JsonResponse({"response": "Password changed successfully"})
        elif request.POST.get("action") == "change_email":
            email = request.POST.get("email").strip()
            if email == request.user.email:
                return JsonResponse({"response": "Email is the same as before"})
            if User.objects.filter(email=email).exists():
                return JsonResponse({"response": "Email already exists"})
            else:
                try:
                    Otp.objects.get(username=request.user.username).delete()
                except:
                    pass
                otp = str(random.randint(100000, 999999))
                new_otp = Otp(username=request.user.username, mail=email, otp=otp)

                new_otp.save()
                send_mail(
                    email,
                    f"ClickViral OTP Verification Code For: {request.user.username}",
                    f"Hello {request.user.username},\n\nYour OTP is {otp}\n\nIf You did not request this code, please ignore this email.\n\nClickViral Team",
                )
                return JsonResponse({"success": "Verify email"})
        elif request.POST.get("action") == "verify_email":
            otp = request.POST.get("otp").strip()
            try:
                otp = Otp.objects.get(username=request.user.username, otp=otp)
                if otp.tries > 10:
                    return JsonResponse({"error": "Otp expired"})

                created = otp.created_at
                now = datetime.now(timezone.utc)
                diff = now - created

                if diff.total_seconds() > 43200:
                    return JsonResponse({"error": "Otp expired"})
                request.user.email = otp.mail
                request.user.save()
                otp.delete()
                return JsonResponse({"response": "Email changed successfully"})
            except:
                return JsonResponse({"error": "Invalid OTP"})
        elif request.POST.get("action") == "verify":
            password = request.POST.get("password")
            if request.user.check_password(password):
                return JsonResponse({"response": "Verified"})
            else:
                return JsonResponse({"error": "Invalid"})

    return render(request, "security.html")
