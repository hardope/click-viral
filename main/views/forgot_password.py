# Desc: View for forgot password
from django.contrib.auth import authenticate, login
from django.http import  JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from ..models import Otp
from .sendmail import send_mail
from datetime import datetime, timezone

def forgot_password(request):
    if request.method == "POST":
        if request.POST.get("action") == "find_account":
            email = request.POST.get("email").strip()
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
            else:
                return JsonResponse({"error": "No account found with this email"})
            try:
                Otp.objects.get(username=user.username).delete()
            except:
                pass
            otp = str(random.randint(100000, 999999))
            new_otp = Otp(username=user.username, mail=email, otp=otp)

            new_otp.save()
            send_mail(
                email,
                f"Password Reset - ClickViral OTP Verification Code For: {user.username}",
                f"Hello {user.username},\n\nYour OTP is {otp}\n\nIf You did not request this code, please ignore this email.\n\nClickViral Team",
            )
            return JsonResponse({"success": "Verify email"})
        elif request.POST.get("action") == "verify_otp":
            otp = request.POST.get("otp").strip()
            email = request.POST.get("email").strip()
            password = request.POST.get("password").strip()
            user = User.objects.get(email=email)
            if user.check_password(password):
                return JsonResponse(
                    {"error": "New password cannot be same as old password"}
                )
            if Otp.objects.filter(otp=otp, mail=email).exists():
                otp = Otp.objects.get(otp=otp, mail=email)
                otp.delete()
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                user = authenticate(request, username=user.username, password=password)
                login(request, user)
                return JsonResponse({"success": "Done"})
            else:
                return JsonResponse({"error": "Invalid OTP"})
    if request.user.is_authenticated:
        try:
            Otp.objects.get(username=request.user.username).delete()
        except:
            pass
        otp = str(random.randint(100000, 999999))
        new_otp = Otp(username=request.user.username, mail=request.user.email, otp=otp)

        new_otp.save()
        send_mail(
            request.user.email,
            f"Password Reset - ClickViral OTP Verification Code For: {request.user.username}",
            f"Hello {request.user.username},\n\nYour OTP is {otp}\n\nIf You did not request this code, please ignore this email.\n\nClickViral Team",
        )

    return render(request, "forgot_password.html")
