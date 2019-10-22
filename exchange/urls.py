from django.urls import path, re_path
from django.conf.urls import url

from . import views

app_name = 'exchange'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('games/', views.games, name='games'),
    path('games/<int:game_id>/', views.game, name='game'),
    path('sell/', views.sell, name='sell'),
    path('success/', views.success, name='success'),
    path('logout/', views.logout_request, name='logout'),
    path('login/', views.login_request, name='login'),
    path('profile/', views.profile, name='profile'),
    path('activation-sent/', views.activation_sent, name='activation_sent'),
    path('activation-successful/', views.activation_successful, name='activation_successful'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('post-denied/', views.post_denied, name='post-denied')
    
]
