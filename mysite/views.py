from django.contrib.auth import logout
from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
def home(request):
    return render(request,'users/home.html')

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request,f'You have been logged out')
        return render(request,'users/home.html')

    def post(self, request):
        logout(request)
        messages.success(request,f'You have been logged out')
        return render(request,'users/home.html')