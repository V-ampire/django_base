from django.urls import path
from . import views

app_name = 'pushes'
urlpatterns = [
    path('', views.PushesIndexView.as_view(), name='pushes_index'),
    path('subscribe', views.SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe', views.UnSubscribeView.as_view(), name='unsubscribe'),
    path('push', views.SendPushView.as_view(), name='push'),
]