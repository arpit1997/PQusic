from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^login/', views.user_login, name="login"),
	url(r'^home/', views.home, name="home"),
	url(r'^signup/', views.user_signup, name="signup"),
	url(r'^activate', views.activate, name="activate"),
	url(r'^password-reset', views.password_reset, name='password_reset'),
	url(r'^change-password', views.change_password, name='change_password')
]
