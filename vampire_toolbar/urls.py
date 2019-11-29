from django.urls import path
from . import views

app_name = 'toolbar'
urlpatterns = [
    path('', views.ToolbarIndexView.as_view(), name='toolbar_index'),
]