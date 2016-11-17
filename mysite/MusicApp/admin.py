from django.contrib import admin
from .models import AppUserProfile,PlaylistSongs,Playlist,History,SongHistory,Followings,Followers

admin.site.register(AppUserProfile)
admin.site.register(SongHistory)
admin.site.register(Playlist)
admin.site.register(History)
admin.site.register(PlaylistSongs)
admin.site.register(Followers)
admin.site.register(Followings)
