from django.shortcuts import redirect
from django.urls import reverse

def login_required(function):

    def wrapper(request, *args):
        if 'user_data' not in request.session:
            return redirect(reverse("my_index"))
        resp = function(request, *args)
        return resp
    
    return wrapper