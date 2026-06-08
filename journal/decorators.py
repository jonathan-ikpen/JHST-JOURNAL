from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def verified_email_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_email_verified:
            messages.warning(request, "Please verify your email address to access this feature. Check your inbox or request a new verification email.")
            return redirect('dashboard')
        return function(request, *args, **kwargs)
    return wrap
