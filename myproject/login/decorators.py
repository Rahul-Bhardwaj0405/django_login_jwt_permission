from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.http import JsonResponse

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        # JWT Authentication
        jwt_auth = JWTAuthentication()
        try:
            user, _ = jwt_auth.authenticate(request)
            request.user = user
        except AuthenticationFailed:
            return JsonResponse({'error': 'Authentication Failed'}, status=401)

        # Throttling for users
        user_throttle = UserRateThrottle()
        anon_throttle = AnonRateThrottle()
        if user.is_authenticated:
            if not user_throttle.allow_request(request, view_func):
                return JsonResponse({'error': 'Request limit exceeded'}, status=429)
        else:
            if not anon_throttle.allow_request(request, view_func):
                return JsonResponse({'error': 'Request limit exceeded'}, status=429)

        # Call the original view
        return view_func(request, *args, **kwargs)

    return wrapper
