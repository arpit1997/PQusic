import binascii
import os
import re
import smtplib
import string
from copy import copy, deepcopy

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response
from django.template.context_processors import csrf
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from bs4 import BeautifulSoup
from .helpers.helper import custom_save, encrypt, decrypt, send_verification_mail, validate_username_email
from .helpers.ytqueryparser import YtQueryParser
from .helpers.ytPlaylistParser import YtPlaylist
from .models import AppUserProfile
from .models import Playlist
from .models import PlaylistSongs, Followers, Followings, SongHistory, History

# encryption key for creating activation key
secret_key = "123456789"
# sender's email address in account verification email
email_address = "shockwavemoto@gmail.com"
# sender;s email password
email_password = "9829667088"


@csrf_exempt
def user_login(request):
	"""
	handle for user login
	:param request:
	:return: httpresponse or rendered template
	"""
	if request.method == "POST":
		print(request.POST)
		username = request.POST.get("username")
		passwd = request.POST.get("password")
		user = authenticate(username=username, password=passwd)
		if user is not None:
			# if user's email has been verified then this will be true. default is false here
			if user.is_active:
				login(request, user)
				x = {'status': "1"}
				import json
				x = json.dumps(x)
				# return HttpResponseRedirect(reverse('musicapp:home'))
				return JsonResponse(x, safe=False)
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
	if request.method == "POST":
		search = request.POST.get("search")

	pl = YtPlaylist()
	# x = pl.yt_playlist['Country']
	# x = x[:3]
	context = {
		'user': request.user,
		'pl': pl.yt_playlist,
	}
	return render(request, "MusicApp/homepage.html", context)


@csrf_exempt
def results_query(request):
	if request.method == "POST":
		query = request.POST.get("query")
		print(query)
		x = ""
		for it in query:
			if it == ' ':
				it = '+'
			elif (it not in string.ascii_lowercase) and (it not in string.ascii_uppercase):
				it = '%' + str(ord(it))
			x += it

		print(x)
		query = x
		query = str(query)
		results = YtQueryParser(query)
		context = {
			'results': results.yt_search_list,
		}
		# print(results.yt_search_list[0].yt_title)
		# print(results.yt_search_list[0].yt_id)
		import json
		x = json.dumps(results.yt_search_json)
		return JsonResponse(x, safe=False)
	# return render(request, "MusicApp/main.html", context)
	else:
		return HttpResponse("Bad request")


@csrf_exempt
def results_query_json(request, query):
	if request.method == "GET":
		query = str(query)
		results = YtQueryParser(query)
		context = {
			'results': results.yt_search_list,
		}
		# print(results.yt_search_list[0].yt_title)
		# print(results.yt_search_list[0].yt_id)
		import json
		x = json.dumps(str(results.yt_search_json))
		return JsonResponse(x)
	# return render(request, "MusicApp/main.html", context)
	else:
		return HttpResponse("Bad request")


def user_signup(request):
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
		print(username, email, passwd, first_name, last_name, sep='$')
		# privacy = request.POST.get("privacy")
		# privacy = bool(privacy)
		# creating user
		user_exists_or_not, message = validate_username_email(username, email)
		if not user_exists_or_not:
			user = User.objects.create_user(username, email, passwd, first_name=first_name, last_name=last_name)
			user = AppUserProfile.objects.create(user=user)
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
			decoded = decoded.decode("utf-8")
		except binascii.Error:
			decoded = None
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


def change_password(request):
	"""
	handle for user account password change functionality
	:param request:
	:return: httpresponseredirect or rendered html
	"""
	user = request.user
	if request.method == "POST":
		print(request.POST)
		username = user.username
		old_password = request.POST.get("old_password")
		new_password = request.POST.get("new_password")
		new_password_again = request.POST.get("new_password_again")
		user = authenticate(username=username, password=old_password)
		print(new_password)
		print(new_password_again)
		if user is not None:
			if str(new_password) == str(new_password_again):
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
		print("get request")
		messages.success(request, "changing password will logout and you have to login again")
		return render(request, "MusicApp/change_password.html", {'user': user})


def user_logout(request):
	print(request.user)
	logout(request)
	return HttpResponseRedirect(reverse("musicapp:home"))


@csrf_exempt
def get_video_url(request, yt_url):
	"""
	also sue a create history function
	:param request:
	:return:
	:To do - don't forget to create history
	"""
	try:
		import pafy
	except ImportError:
		print("Can not import Pafy")
	if request.method == "GET":
		video_id = yt_url
		yt_url = "http://youtube.com/watch?v=" + yt_url
		print(yt_url)
		video = pafy.new(yt_url)
		audio = video.audiostreams
		audio_url = audio[0].url
		print(audio_url)
		if request.user.is_authenticated():
			print("in if")
			r = requests.get(yt_url)
			print(r.status_code)
			page = r.text
			soup = BeautifulSoup(page, 'html.parser')
			span_title = soup.find_all('span', {'class': 'watch-title'})
			print(span_title)
			title = span_title[0]['title']
			print(title)
			new_song_history, _ = SongHistory.objects.get_or_create(song_id=video_id, song_name=title,
																	last_listened=timezone.now())
			new_song_history.save()
			user = request.user
			history_object, _ = History.objects.get_or_create(user=user)
			history_object.save()
			history_object.song.add(new_song_history)
			history_object.save()
		return HttpResponse(audio_url)
	else:
		return HttpResponse("NULL")


def view_user_profile(request):
	if request.method == "GET":
		user = request.user
		name = user.first_name + " " + user.last_name
		email = user.email
		followers_count = 0
		followings_count = 0
		try:
			follower_object = Followers.objects.get(follower_user=user)
		except ObjectDoesNotExist:
			follower_object = None
		if follower_object is not None:
			followers_count = follower_object.followers.all().count()
		try:
			following_object = Followings.objects.get(following_user=user)
		except ObjectDoesNotExist:
			following_object = None
		if following_object is not None:
			followings_count = following_object.followings.all().count()
		context = {
			'name': name,
			'email': email,
			'followers': followers_count,
			'followings': followings_count,
		}
		return render(request, "MusicApp/profile.html", context)


@csrf_exempt
def search_users(request):
	"""f
	just use a filter query
	use a GET request
	:param request
	:return a list of relevent users:
	use some regex
	"""
	print("hello")
	if request.method == "POST":
		query = request.POST.get('query')
		relevent_users = User.objects.filter(username__icontains=query)[:10]
		print(relevent_users)
		context = {
			'users': relevent_users,
		}
		return render(request, "MusicApp/users_list.html", context)
	else:
		return render(request, "MusicApp/users_list.html")


@login_required
def create_playlist(request):
	"""
	create playlist
	:param request:
	:return:
	"""
	if request.method == "POST":
		user = request.user
		playlist_name = request.POST.get('name')
		print(playlist_name)
		privacy = bool(request.POST.get('privacy'))
		try:
			p = Playlist.objects.get(user=user, playlist_name=playlist_name)
		except ObjectDoesNotExist:
			p = None
		if p is None:
			new_playlist = Playlist(user=user, playlist_name=playlist_name, privacy=privacy)
			new_playlist.save()
			return HttpResponseRedirect(reverse("musicapp:view-playlists"))
		else:
			messages.error(request, "playlist already exists")
			return render(request, "MusicApp/create_playlist.html")
	else:
		return render(request, "MusicApp/create_playlist.html")


@login_required
def delete_playlist(request, name):
	"""
	name parameter is case sensitive ve careful
	:param request:
	:param name:
	:return:
	"""
	if request.method == "GET":
		user = request.user
		playlist_name = name
		try:
			playlist = Playlist.objects.get(user=user, playlist_name=playlist_name)
		except ObjectDoesNotExist:
			playlist = None
		if playlist is not None:
			playlist.delete()
			return HttpResponseRedirect(reverse("musicapp:view-playlists"))
		else:
			return HttpResponse("playlist Does not exist")
	else:
		return HttpResponse("Bad request")


@login_required
def add_to_playlist(request):
	"""
	adds a song to playlist
	request type can be decided from discussion with front-end people
	:param request:
	:return:
	"""
	if request.method == "POST":
		user = request.user
		playlist_name = request.POST.get('name')
		try:
			playlist = Playlist.objects.get(user=user, playlist_name=playlist_name)
		except ObjectDoesNotExist:
			playlist = None
		if playlist is not None:
			song_id = request.POST.get('song_id')
			song_name = request.POST.get('song_name')
			try:
				mood = request.POST.get('mood')
			except KeyError:
				mood = None
			try:
				song = PlaylistSongs.objects.get(song_id=song_id)
			except ObjectDoesNotExist:
				song = None
			if song is None:
				song = PlaylistSongs(song_id=song_id, song_name=song_name, mood=mood)
				song.save()
				playlist.songs.add(song)
				playlist.save()
				messages.success(request, "song added")
				return HttpResponseRedirect(reverse("musicapp:view-playlists"))
			else:
				playlist.songs.add(song)
				playlist.save()
				messages.success(request, "song added")
				return HttpResponseRedirect(reverse("musicapp:view-playlists"))
		else:
			return HttpResponse("Playlist does not exist")


def add_to_playlist_router(request, song_id):
	user = request.user
	if request.user:
		pl = Playlist.objects.filter(user__username=user.username)
		# scraper
		yt_url = "https://www.youtube.com/watch?v=" + song_id
		r = requests.get(yt_url)
		soup = BeautifulSoup(r.text, 'html.parser')
		span_tag = soup.find_all('span', {'class': 'watch-title'})
		span_tag = span_tag[0]
		print(span_tag)
		title = span_tag.get_text()
		print(title)
		# scrpaer
		context = {
			'playlists': pl,
			'song_id': song_id,
			'title': title,
		}
		return render(request, "MusicApp/add_to_playlist.html", context)


def remove_from_playlist(request, playlist_name, song_id):
	if request.method == "GET":
		user = request.user
		song_id = song_id
		print(song_id)
		playlist_name = playlist_name
		try:
			playlist = Playlist.objects.get(user=user, playlist_name=playlist_name)
		except ObjectDoesNotExist:
			playlist = None
		if playlist is not None:
			try:
				song = PlaylistSongs.objects.get(song_id=song_id)
			except ObjectDoesNotExist:
				song = None
			if song is not None:
				playlist.songs.remove(song)
				playlist.save()
				messages.success(request, "song deleted")
				return HttpResponseRedirect(reverse("musicapp:playlist_songs", args=(playlist_name,)))
			else:
				return HttpResponse("song not found")
		else:
			return HttpResponse("playlist not found")


def view_playlists(request):
	"""
	working
	:param request:
	:return:
	"""
	if request.method == "GET":
		user = request.user
		playlists = Playlist.objects.filter(user__username=user.username)
		playlist_attr = []
		"""
		fetching attributes
		playlist_name = playlists[0].playlist_name
		playlist_name = playlists[1].playlist_name

		To get count of songs in every playlist do
		count = playlists[0].songs.count()
		"""
		for playlist in playlists:
			n = playlist.playlist_name
			c = playlist.songs.all().count()
			playlist_attr.append((n, c))
			print(c)
		context = {
			"playlists": playlist_attr
		}
		return render(request, "MusicApp/playlist.html", context)


def view_playlist_songs(request, playlist_name):
	print("view playlist songs")
	if request.method == "GET":
		playlist_name = str(playlist_name)
		user = request.user
		try:
			playlist = Playlist.objects.get(user=user, playlist_name=playlist_name)
		except ObjectDoesNotExist:
			playlist = None
		print(playlist)
		if playlist is not None:
			songs = playlist.songs.all()
			for song in songs:
				print(song.song_name)
		context = {
			'name': playlist_name,
			'songs': songs,
			'privacy': playlist.privacy
		}
		return render(request, "MusicApp/song_list.html", context)


def view_history(request):
	pass


def follow_user(request, username):
	if request.method == "GET":
		# user = the user logged in
		user = request.user
		# user wants to follow the followers_user
		follower_user = str(username)
		follow, created = Followers.objects.get_or_create(follower_user=user)
		follow.save()
		if follow.followers.filter(followers__followers__username=follower_user).exists():
			return HttpResponse("already followed")
		else:
			follower_user_object, _ = User.objects.get_or_create(username=follower_user)
			follow.followers.add(follower_user_object)
			follow.save()
			reverse_follow_method(request, username)
			return HttpResponse("follow successful")


def reverse_follow_method(request, username):
	user = request.user
	following_user = User.objects.get(username=username)
	following, _ = Followings.objects.get_or_create(following_user=following_user)
	following.save()
	following.followings.add(user)
	following.save()


def unfollow_user(request, username):
	if request.method == "GET":
		user = request.user
		unfollower_user = username
		follow = Followers.objects.get(follower_user=user)
		if follow.followers.filter(followers__followers__username=unfollower_user).count() != 0:
			follow.followers.remove(unfollow_user)
			follow.save()
			return HttpResponse("unfollowed")
		else:
			return HttpResponse("user does not exist")


def view_user_playlists(request, username):
	if request.method == "GET":
		user = User.objects.get(username=username)
		playlists = Playlist.objects.filter(user__username=user.username)
		playlist_attr = []
		"""
		fetching attributes
		playlist_name = playlists[0].playlist_name
		playlist_name = playlists[1].playlist_name

		To get count of songs in every playlist do
		count = playlists[0].songs.count()
		"""
		for playlist in playlists:
			n = playlist.playlist_name
			c = playlist.songs.all().count()
			playlist_attr.append((n, c))
			print(c)
		context = {
			"playlists": playlist_attr,
			'uname': username,
		}
		return render(request, "MusicApp/user_playlist.html", context)


def view_user_playlist_songs(request, username, playlist_name):
	if request.method == "GET":
		print("view user playlist songs")
		playlist_name = str(playlist_name)
		user = User.objects.get(username=username)
		print(user)
		try:
			playlist = Playlist.objects.get(user=user, playlist_name=playlist_name)
		except ObjectDoesNotExist:
			playlist = None
		if playlist is not None:
			print("playlistNot None")
			songs = playlist.songs.all()
			print(songs)
		context = {
			'name': playlist_name,
			'songs': songs,
			'privacy': playlist.privacy,
			'uname': username,
		}
		return render(request, "MusicApp/song_list.html", context)


def list_followers(request):
	pass


def list_followings(request):
	pass


def modify_mood_of_song(request):
	pass


def share_playlist_router(request, playlist_name):
	if request.method == "GET":
		user = request.user
		try:
			follow_object = Followers.objects.get(follower_user=user)
		except ObjectDoesNotExist:
			return HttpResponse("you do't follow anyone so you can't share")
		followers_list = follow_object.followers.all()
		context = {
			'followers': followers_list,
			'playlist_name': playlist_name
		}
		return render(request, "MusicApp/share.html", context)
	else:
		return HttpResponse("Bad request")


def share_playlist(request, playlist_name):
	if request.method == "POST":
		username_share = request.POST.get("username")
		user_share = User.objects.get(username=username_share)
		email_share = user_share.email
		msg = request.user.username + " shared playlist " + playlist_name + " with you"
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login("shockwavemoto@gmail.com", "9829667088")
		server.sendmail(email_address, email_share, msg)
		server.quit()
		messages.success(request, "shared successfully")
		return HttpResponseRedirect(reverse("musicapp:view-playlists"))


def import_playlist(request, username, name):
	user = request.user
	try:
		pl_object = Playlist.objects.get(user=user, playlist_name=name)
	except ObjectDoesNotExist:
		pl_object = None
	if pl_object is None:
		user_playlist = Playlist.objects.get(user__username=username, playlist_name=name)
		new_imported_playlist = Playlist(user=user, playlist_name=name, privacy=True)
		new_imported_playlist.save()
		songs = user_playlist.songs.all()
		print(songs)
		for song in songs:
			print(song)
			new_imported_playlist.songs.add(song)
		print("view:import playlist")
		new_imported_playlist.save()
		messages.success(request, "playlist imported")
		return HttpResponseRedirect(reverse("musicapp:view-playlists"))
	else:
		messages.error(request, "playlist with this name already exist")
		return HttpResponseRedirect(reverse("musicapp:view-playlists"))


# test view .
def hello(request, name):
	return HttpResponse(str(name))
