# Description: Views for chat
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Chat, User_notification
root = "/home/clickviral/clickviral"

def chat(request, query):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        if query == "users":
            return render(
                request,
                "chat.html",
                {
                    "tab": "users",
                },
            )
        try:
            user = User.objects.get(username=query)
        except:
            return render(request, "nopage.html")
        return render(
            request,
            "chat.html",
            {
                "tab": user.username,
            },
        )


def get_chats(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        chats = Chat.objects.filter(sender=request.user)
        chats1 = Chat.objects.filter(recipient=request.user)
        chats = [i.to_dict()["recipient"] for i in chats] + [
            i.to_dict()["sender"] for i in chats1
        ]
        chats = list(set(chats))

        return JsonResponse(chats, safe=False)


def get_messages(request, query):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        username, count = query.split("-")
        user = User.objects.get(username=username)
        chats = Chat.objects.filter(
            Q(sender=request.user, recipient=user)
            | Q(recipient=request.user, sender=user)
        ).order_by("created_at")
        chats = [i.to_dict() for i in chats]
        if count != "0":
            chats = chats[int(count) :]

        try:
            notification = User_notification.objects.get(user=request.user, notify=user)
            notification.delete()
        except:
            pass

        return JsonResponse(chats, safe=False)


def send_message(request):
    if not request.user.is_authenticated:
        return HttpResponse("...")
    if request.method == "POST":
        if request.POST.get("recipient") == request.user.username:
            return HttpResponse("...")
        else:
            try:
                recipient = User.objects.get(username=request.POST.get("recipient"))
            except:
                return HttpResponse("...")
            try:
                media_file = request.FILES.get("media")
                media = str(media_file).split(".")[1]
                assert media_file is not None
                new_message = Chat(
                    sender=request.user,
                    recipient=recipient,
                    message=request.POST.get("message"),
                    media=media,
                )
                new_message.save()
                with open(
                    f"{root}/media/chats/{new_message.id}.{media}", "wb+"
                ) as file:
                    for chunk in media_file.chunks():
                        file.write(chunk)

                User_notification.objects.create(user=recipient, notify=request.user)
            except:
                if request.POST.get("message") != "":
                    new_message = Chat(
                        sender=request.user,
                        recipient=recipient,
                        message=request.POST.get("message"),
                    )
                User_notification.objects.create(user=recipient, notify=request.user)
            if request.POST.get("message") != "":
                new_message.save()
            return HttpResponse("...")
