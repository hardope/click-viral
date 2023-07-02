# Description: Search view
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User

def search(request):
    if not request.user.is_authenticated:
        return JsonResponse([], safe=False)

    if request.method == "POST":
        query = request.POST.get("search").strip()
        users = User.objects.filter(
            Q(username__icontains=query)
            | Q(email__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
        users = [i.username for i in users]
        return JsonResponse(users, safe=False)