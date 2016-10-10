import base64
import binascii
import os
import re
import smtplib

from Crypto.Cipher import XOR
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import timezone

# encryption key for creating activation key
secret_key = os.environ.get("encryption_key")
# sender's email address in account verification email
email_address = os.environ.get("email")
# sender;s email password
email_password = os.environ.get("password_a")


def user_login(request):
	"""
	handle for user login
	:param request:
	:return: httpresponse or rendered template
	"""
	if request.method == "POST":
		username = request.POST.get("username")
		passwd = request.POST.get("password")
		user = authenticate(username=username, password=passwd)
		if user is not None:
			# if user's email has been verified then this will be true. default is false here
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('musicapp:home'))
			else:
				return HttpResponseRedirect(reverse('musicapp:activate'))
		else:
			messages.error(request, "username and password did not match")
			return render(request, "MusicApp/user_login.html")

	# for a GET request
	else:
		return render(request, "MusicApp/user_login.html")


def home(request):
	"""
	homepage of MusicApp
	:param request:
	:return: render(html)

	:To do: implement this function prperly
	"""
	# import pafy
	# url = "https://www.youtube.com/watch?v=PT2_F-1esPk"
	# video = pafy.new(url)
	# audio = video.audiostreams
	# yt_url = audio[0].url

	context = {
		'user': request.user,
	}
	return render(request, "MusicApp/homepage.html", context)


def user_signup(request):
	# if user has submitted a form
	"""
	handle for user sign up
	:param request:
	:return: httpresponse or rendered html
	:To do: generate unique key according to time function or etc

	"""
	if request.method == "POST":
		# extracting form's data submitted by user
		username = request.POST.get("username")
		email = request.POST.get("email")
		passwd = request.POST.get("passwd")
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		# creating user
		user_exists_or_not, message = validate_username_email(username, email)
		if not user_exists_or_not:
			user = User.objects.create_user(username, email, passwd, first_name=first_name, last_name=last_name)
			# custom save for creating non active user
			custom_save(user)
			activation_key = encrypt(secret_key, email)
			# sending account verification mail
			message = "Your Email address is" + email + "activation key is " + activation_key.decode("utf-8")
			send_verification_mail(email, activation_key, message)
			return HttpResponseRedirect(reverse("musicapp:activate"))
		else:
			messages.error(request, message)
			return render(request, "MusicApp/user_signup.html")

	# for a GET request
	else:
		return render(request, "MusicApp/user_signup.html")


def activate(request):
	"""
	handle for user account activation
	:param request:
	:return: httpresponseredirect or rendered html

	"""
	if request.method == "POST":
		email = request.POST.get("email")
		activation_key = request.POST.get("key")
		# verifying thw activation key
		try:
			decoded = decrypt(secret_key, activation_key)
		except binascii.Error:
			decoded = None
		decoded = decoded.decode("utf-8")
		if email == decoded:
			user = User.objects.get(email=email)
			if user is None:
				messages.error(request, "This email id is not valid")
				return render(request, 'MusicApp/activation_form.html')
			# activating the user
			else:
				user.is_active = True
				user.save()
				messages.success(request, "account activated successfully please Login Now")
				return HttpResponseRedirect(reverse("musicapp:login"))
		else:
			messages.error(request, "wrong activation key")
			return render(request, 'MusicApp/activation_form.html')
	else:
		return render(request, 'MusicApp/activation_form.html')


def password_reset(request):
	"""
	handle for user account password reset functionality
	:param request:
	:return: httpresponseredirect or rendered html
	:To do: generate unique key everytime a user request for password reset

	"""
	if request.method == 'POST':
		email = request.POST.get("email")
		re_expression = re.match(r'(.*)@(.*?)', email)
		email_user_name = re_expression.group(1)
		current_time = str(timezone.now())
		key_text = email_user_name + current_time
		new_password = encrypt(secret_key, key_text).decode("utf-8")
		message = str(new_password)
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			user = None
		if user is not None:
			user.set_password(new_password)
			user.save()
			send_verification_mail(email, new_password, message)
			messages.success(request, "new password has been sent to your email please login with given password")
			return HttpResponseRedirect(reverse("musicapp:login"))
		else:
			messages.error(request, "Sorry this email address is incorrect")
			return render(request, "MusicApp/password_reset.html")
	else:
		return render(request, "MusicApp/password_reset.html")


@login_required
def change_password(request):
	"""
	handle for user account password change functionality
	:param request:
	:return: httpresponseredirect or rendered html
	"""
	user = request.user
	if request.method == "POST":
		username = user.username
		old_password = request.POST.get("old_password")
		new_password = request.POST.get("new_password")
		new_password_again = request.POST.get("new_password_again")
		user = authenticate(username=username, password=old_password)
		if user is not None:
			if new_password == new_password_again:
				user.set_password(new_password)
				user.save()
				logout(request)
				messages.success(request, "password has been changed successfully now login")
				return HttpResponseRedirect(reverse("musicapp:login"))
			else:
				messages.error(request, "new password you entered did not match")
				return render(request, "MusicApp/change_password.html", {'user': user})
		else:
			messages.error(request, "sorry the password you entered is not correct")
			return render(request, "MusicApp/change_password.html", {'user': user})
	else:
		messages.success(request, "changing password will logout and you have to login again")
		return render(request, "MusicApp/change_password.html", {'user': user})

def get_video_url(request):

	try:
		import pafy
	except:
		pass
	if request.method == "POST":
		yt_url = request.POST.get("yt_url")
		video = pafy.new(yt_url)
		audio = video.audiostreams
		audio_url = audio[0].url
		return HttpResponse(audio_url)
	else:
		return HttpResponse("NULL")


# ******************************************** #
# helper functions
# ********************************************* #

def custom_save(user):
	"""
	custom save function for creating non active user
	checking a user is active or not
	:param user:
	"""
	user.is_active = False
	user.save()


def encrypt(key, plaintext):
	"""
	encrypt a string and return
	:param key:
	:param plaintext:
	:return: unicode(encryptedtext)
	"""
	cipher = XOR.new(key)
	return base64.b64encode(cipher.encrypt(plaintext))


def decrypt(key, ciphertext):
	"""
	decrypt a string with key and return
	:param key:
	:param ciphertext:
	:return:decrypted text
	"""
	cipher = XOR.new(key)
	return cipher.decrypt(base64.b64decode(ciphertext))


def send_verification_mail(email, activation_key, msg):
	"""
	send verification mail for new registered user
	:param email:
	:param activation_key:
	:param msg:
	"""
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(email_address, email_password)
	server.sendmail(email_address, email, msg)
	server.quit()


def validate_username_email(username, email):
	"""
	check user exists or not
	:param username:
	:param email:
	:return:boolean, message
	"""
	try:
		user_name = User.objects.get(username=username)
	except User.DoesNotExist:
		user_name = None

	try:
		e_mail = User.objects.get(email=email)
	except User.DoesNotExist:
		e_mail = None

	print(user_name)
	print(e_mail)

	if user_name is None and e_mail is None:
		user_exists_or_not = False
		message = ""
	else:
		if user_name is None and e_mail is not None:
			user_exists_or_not = True
			message = "A user is already regsitered with this email address"
		else:
			if user_name is not None and e_mail is None:
				user_exists_or_not = True
				message = "username already exists"
			else:
				user_exists_or_not = True
				message = "username and email already exists"

	return user_exists_or_not, message
