import smtplib
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from Crypto.Cipher import AES, XOR
import base64
import os
secret_key = os.environ.get("encryption_key")
email_address = os.environ.get("email")
email_password = os.environ.get("password_a")


def user_login(request):
	if request.method == "POST":
		username = request.POST.get("username")
		passwd = request.POST.get("password")
		user = authenticate(username=username, password=passwd)
		if user is not None:
			if user.is_active :
				login(request, user)
				return HttpResponse("success")
		else:
			messages.error(request, "username and password did not match")
			return render(request, "MusicApp/user_login.html")

	else:
		return render(request, "MusicApp/user_login.html")


def home(request):
	pass


def user_signup(request):
	if request.method == "POST":
		username = request.POST.get("username")
		email = request.POST.get("email")
		passwd = request.POST.get("passwd")
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		user = User.objects.create_user(username,email,passwd,first_name=first_name,last_name=last_name)
		custom_save(user)
		activation_key = encrypt(secret_key,email)
		send_verification_mail(email, activation_key)
		return HttpResponseRedirect(reverse("musicapp:activate"))

	else:
		return render(request, "MusicApp/user_signup.html")


def activate(request):
	if request.method == "POST":
		email = request.POST.get("email")
		activation_key = request.POST.get("key")
		decoded = decrypt(secret_key, activation_key)
		decoded = decoded.decode("utf-8")
		if email == decoded:
			user = User.objects.get(email=email)
			if user is None:
				print("none user")
			user.is_active = True
			user.save()
			return HttpResponse("account activated successfully")
		else:
			return HttpResponse("failed")
	else:
		return render(request, 'MusicApp/activation_form.html')


# <---------------------------->
# helper functions

def custom_save(user):
	user.is_active = False
	user.save()


def encrypt(key, plaintext):
	cipher = XOR.new(key)
	return base64.b64encode(cipher.encrypt(plaintext))


def decrypt(key, ciphertext):
	cipher = XOR.new(key)
	return cipher.decrypt(base64.b64decode(ciphertext))


def send_verification_mail(email, activation_key):
		server = smtplib.SMTP('smtp.gmail.com',587)
		server.starttls()
		server.login(email_address,email_password)
		msg = "Your Email address is"+email+"activation key is "+activation_key.decode("utf-8")
		server.sendmail(email_address, email, msg)
		server.quit()
