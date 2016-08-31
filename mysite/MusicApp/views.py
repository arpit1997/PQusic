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
# encryption key for creating activation key
secret_key = os.environ.get("encryption_key")
# sender's email address in account verification email
email_address = os.environ.get("email")
# sender;s email password
email_password = os.environ.get("password_a")


# View to handle user login
def user_login(request):
	# if user has submitted a form for login
	if request.method == "POST":
		username = request.POST.get("username")
		passwd = request.POST.get("password")
		user = authenticate(username=username, password=passwd)
		if user is not None:
			# if user's email has been verfied then this will be true. default is false here
			if user.is_active :
				login(request, user)
				return HttpResponse("success")
		else:
			messages.error(request, "username and password did not match")
			return render(request, "MusicApp/user_login.html")

	# for a GET request
	else:
		return render(request, "MusicApp/user_login.html")


# homepage of MusicApp yet to be implemented
def home(request):
	pass


# view to handle user sign up
def user_signup(request):
	# if user has submitted a form
	if request.method == "POST":
		# extracting form's data submitted by user
		username = request.POST.get("username")
		email = request.POST.get("email")
		passwd = request.POST.get("passwd")
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		# creating user
		user = User.objects.create_user(username,email,passwd,first_name=first_name,last_name=last_name)
		# custom save for creating non active user
		custom_save(user)
		activation_key = encrypt(secret_key,email)
		# sending account verification mail
		send_verification_mail(email, activation_key)
		return HttpResponseRedirect(reverse("musicapp:activate"))

	# for a GET request
	else:
		return render(request, "MusicApp/user_signup.html")


def activate(request):
	# if user has submitted a form for activation of an account
	if request.method == "POST":
		email = request.POST.get("email")
		activation_key = request.POST.get("key")
		# verifying thw activation key
		decoded = decrypt(secret_key, activation_key)
		decoded = decoded.decode("utf-8")
		if email == decoded:
			user = User.objects.get(email=email)
			if user is None:
				print("none user")
			# activating the user
			user.is_active = True
			user.save()
			return HttpResponse("account activated successfully")
		else:
			return HttpResponse("failed")
	else:
		return render(request, 'MusicApp/activation_form.html')


# <---------------------------->
# helper functions


# custom save function for creating non active user
def custom_save(user):
	user.is_active = False
	user.save()


# encrypt function for creating activation keys
def encrypt(key, plaintext):
	cipher = XOR.new(key)
	return base64.b64encode(cipher.encrypt(plaintext))


# for decryption of activation keys
def decrypt(key, ciphertext):
	cipher = XOR.new(key)
	return cipher.decrypt(base64.b64decode(ciphertext))


# simple function for sending verification mails
def send_verification_mail(email, activation_key):
		server = smtplib.SMTP('smtp.gmail.com',587)
		server.starttls()
		server.login(email_address,email_password)
		msg = "Your Email address is"+email+"activation key is "+activation_key.decode("utf-8")
		server.sendmail(email_address, email, msg)
		server.quit()
