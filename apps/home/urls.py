# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('gettime/', views.get_time, name='get_time'),
    path('FirmwareManagement/', views.FirmewareManagement, name='FirmwareManagementURL'),
    # path('change_firmware_action/', views.change_firmware_action, name='change-firmware-action-URL'),
    # path('FirmwareUpload/', views.model_form_upload, name='FirmwareUploadURL'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]