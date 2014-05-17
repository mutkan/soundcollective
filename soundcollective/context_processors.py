# context processors

from notifications.models import Notifications

# include notifications in all views
def notifications(request):
    if request.user.is_authenticated(): 
        return {"notifications": Notifications.objects.filter(user=request.user).order_by('-created_date')[:8]}
    else:
        return {}
