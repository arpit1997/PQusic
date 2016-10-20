import base64
import os
import smtplib

from Crypto.Cipher import XOR
from django.contrib.auth.models import User

# ******************************************** #
# helper functions
# ********************************************* #
# encryption key for creating activation key
secret_key = os.environ.get("encryption_key")
# sender's email address in account verification email
email_address = os.environ.get("email")
# sender;s email password
email_password = os.environ.get("password_a")

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
	print("send verificaion mail")
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
