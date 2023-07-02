# Description: Edit profile view.
from django.http import HttpResponse, JsonResponse
from .models import Profile

root = "/home/ubuntu/viral"
# Create your views here.


def edit_profile(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.POST.get("username") == request.user.username:
                if request.POST.get("action") == "upload":
                    username = request.POST.get("username")
                    profile = Profile.objects.get(user=request.user)
                    try:
                        os.remove(f"{root}/media/profile/{username}.{profile.image}")
                    except:
                        pass
                    profile.image = str(request.FILES.get("image")).split(".")[1]
                    profile.save()
                    with open(
                        f"{root}/media/profile/{username}.{profile.image}", "wb+"
                    ) as file:
                        for chunk in request.FILES.get("image").chunks():
                            file.write(chunk)
                    return JsonResponse({"image": f"{username}.{profile.image}"})
                elif request.POST.get("action") == "about":
                    profile = Profile.objects.get(user=request.user)
                    profile.about = request.POST.get("data")
                    profile.save()
                    return JsonResponse({"data": profile.about})
                elif request.POST.get("action") == "birthday":
                    profile = Profile.objects.get(user=request.user)
                    profile.birthday = request.POST.get("birthday")
                    profile.birthyear = request.POST.get("birthyear")
                    profile.save()
                    return JsonResponse(
                        {"birthday": profile.birthday, "birthyear": profile.birthyear}
                    )
                elif request.POST.get("action") == "gender":
                    profile = Profile.objects.get(user=request.user)
                    profile.gender = request.POST.get("data")
                    profile.save()
                    return JsonResponse({"data": profile.gender})
                elif request.POST.get("action") == "location":
                    profile = Profile.objects.get(user=request.user)
                    profile.location = request.POST.get("data")
                    profile.save()
                    return JsonResponse({"data": profile.location})
                else:
                    return JsonResponse({"image": "empty"})
            else:
                return HttpResponse("...")
        else:
            return HttpResponse("...")
