from functools import wraps
from django.shortcuts import redirect

# decorators.py
from django.urls import resolve

def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check if user is logged in
        if 'logged_in_user' in request.session:
            # User is logged in, execute the original view function
            return view_func(request, *args, **kwargs)
        else:
            # Get the resolved view name
            resolved_view_name = resolve(request.path_info).url_name
            print("Resolved view name:", resolved_view_name)
            # Exclude signup view from redirection
            if resolved_view_name == 'signup':
                return view_func(request, *args, **kwargs)
            # User is not logged in, redirect to login page
            print("Redirecting to login page...")
            return redirect('login')  # Adjust 'login' to your login URL name

    return _wrapped_view
