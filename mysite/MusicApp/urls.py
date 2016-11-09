from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^login/', views.user_login, name="login"),
	url(r'^home/', views.home, name="home"),
	url(r'^signup/', views.user_signup, name="signup"),
	url(r'^activate', views.activate, name="activate"),
	url(r'^password-reset', views.password_reset, name='password_reset'),
	url(r'^change-password', views.change_password, name='change_password'),
	url(r'^view-profile', views.view_user_profile, name='user_profile'),
	# url(r'^(?P<name>[a-zA-Z]{1,})', views.hello, name='hello'),
	# Test view url
	url(r'^playlists$', views.view_playlists, name="view-playlists"),
	url(r'^playlists/$', views.view_playlists, name="view-playlists"),
	url(r'^playlists/create', views.create_playlist, name="create-playlists"),
	url(r'^playlists/delete/(?P<name>[a-zA-Z]{1,})', views.delete_playlist, name="delete-playlist"),
	url(r'^follow/(?P<username>[a-zA-Z0-9]{1,})', views.follow_user, name="follow-user"),
	url(r'^unfollow/(?P<username>[a-zA-Z0-9]{1,})', views.unfollow_user, name="unfollow-user"),
	url(r'^search', views.results_query, name="search-result")
]
