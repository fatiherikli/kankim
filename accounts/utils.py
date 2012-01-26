from accounts.models import UserProfile

def me(request):
    return UserProfile.objects.get(user=request.user)