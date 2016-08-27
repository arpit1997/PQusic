from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render


def user_login(request):
	if request.method == "POST":
		username = request.POST.get("username")
		passwd = request.POST.get("password")
		user = authenticate(username=username, password=passwd)
		if user is not None:
			print("hello")
			login(request, user)
			return HttpResponse("success")
		else:
			# messages.error(request, "username and password did not match")
			return render(request, "MusicApp/user_login.html")

	else:
		return render(request, "MusicApp/user_login.html")


def home(request):
	pass