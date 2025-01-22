from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from login.decorators import login_required

@login_required
def article_list(request):
    # You can access the user details in the request object, including the username
    username = request.user.username
    return JsonResponse({"message": f"Here are the articles, User: {username}"})
