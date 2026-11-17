from django.shortcuts import redirect

def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("accounts:login")
            if request.user.role not in allowed_roles:
                return redirect("accounts:login")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
