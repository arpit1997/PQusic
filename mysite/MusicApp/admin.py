from django.contrib import admin
from .models import AppUserProfile,PlaylistSongs,Playlist,History,SongHistory

admin.site.register(AppUserProfile)
admin.site.register(SongHistory)
admin.site.register(Playlist)
admin.site.register(History)
admin.site.register(PlaylistSongs)
