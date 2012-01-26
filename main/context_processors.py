from accounts.utils import me
from main.forms import LoginForm

def profile(request):
    return {
    'me' : me(request) if request.user.is_authenticated() else False,
    }
