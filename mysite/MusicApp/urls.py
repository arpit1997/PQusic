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
	url(r"^u-logout", views.user_logout, name="logout"),
	# url(r'^(?P<name>[a-zA-Z]{1,})', views.hello, name='hello'),
	# Test view url
	url(r'^playlists$', views.view_playlists, name="view-playlists"),
	url(r'^playlists/$', views.view_playlists, name="view-playlists"),
	url(r'^playlist/(?P<playlist_name>[a-zA-Z0-9]+)$', views.view_playlist_songs, name="playlist_songs"),
	url(r'^playlist/(?P<playlist_name>[a-zA-Z0-9]+)/$', views.view_playlist_songs, name="playlist_songs"),
	url(r'^playlists/create$', views.create_playlist, name="create-playlists"),
	url(r'^playlists/create/$', views.create_playlist, name="create-playlists"),
	url(r'^playlists/add$', views.add_to_playlist, name="add_to_playlist"),
	url(r'^playlists/add/$', views.add_to_playlist, name="add_to_playlist"),
	url(r'^playlist/add/song/(?P<song_id>[\S]+)$', views.add_to_playlist_router, name="add_to_playlist_router"),
	url(r'^playlist/add/song/(?P<song_id>[\S]+)$/', views.add_to_playlist_router, name="add_to_playlist_router"),
	url(r'^playlists/delete/(?P<name>[a-zA-Z]{1,})', views.delete_playlist, name="delete-playlist"),
	url(r'^playlists/(?P<playlist_name>[a-zA-Z0-9]{1,})/songs/(?P<song_id>[a-zA-Z0-9]{1,})', views.remove_from_playlist, name="delete-songs"),
	url(r'^follow/(?P<username>[a-zA-Z0-9]{1,})', views.follow_user, name="follow-user"),
	url(r'^unfollow/(?P<username>[a-zA-Z0-9]{1,})', views.unfollow_user, name="unfollow-user"),
	url(r'^search$', views.results_query, name="search-result"),
	url(r'^search/$', views.results_query, name="search-result"),
	url(r'^audio/geturl/(?P<yt_url>[\S]+)', views.get_video_url, name="get_url"),
	url(r'^audio/geturl/$', views.get_video_url, name="get_url"),
	url(r'^searchuser$', views.search_users, name="search_user"),
	url(r'^searchuser/$', views.search_users, name="search_user")
]
