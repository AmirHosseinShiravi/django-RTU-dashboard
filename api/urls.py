from os import system
from django.urls import path, include
from api.views import systemStatus
urlpatterns=[
    path('SystemStatus/', systemStatus, name='get_system_status'),
]