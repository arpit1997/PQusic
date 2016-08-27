from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^login/', views.user_login, name="login"),
	url(r'^home/', views.home, name="home")
]
