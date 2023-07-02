# Description: View for Notification
from django.http import JsonResponse
from .models import User_notification

def notification(request):

    notifications = User_notification.objects.filter(user=request.user).order_by('created_at')
    notifications = [i.parse() for i in notifications]
    
    return JsonResponse(notifications, safe=False)