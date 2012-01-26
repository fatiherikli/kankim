from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from kankim.accounts.utils import me
from accounts.models import Friendship

def search(request, template='search.html'):
        keyword = request.GET.get('keyword')
        result = User.objects.filter( Q(username__contains=keyword) \
                                     | Q(first_name__contains=keyword) \
                                     | Q(email=keyword) )

        ctx = {
            "keyword" : keyword,
            "result" : result
        }
        return render_to_response(template, RequestContext(request, ctx))


def accept(request, username):
    friend = get_object_or_404(User, username = username)
    friendship = get_object_or_404(Friendship, from_friend = friend, to_friend = request.user)
    me(request).accept_friendship_request(friendship)
    if request.is_ajax():
        return HttpResponse("True")
    else:
        return HttpResponseRedirect("/friends")


def my_friends(request):
    return render_to_response("my_friends.html", context_instance=RequestContext(request) )

def add(request, username):
    friend = get_object_or_404(User, username = username)
    me(request).add_friend(friend)
    if request.is_ajax():
        return HttpResponse("True")
    else:
        return HttpResponseRedirect("/friends")


def cancel(request, username):
    friend = get_object_or_404(User, username = username)
    friendship = get_object_or_404(Friendship, from_friend = friend, to_friend = request.user)
    me(request).cancel_friendship_request(friendship)
    if request.is_ajax():
        return HttpResponse("True")
    else:
        return HttpResponseRedirect("/friends")

