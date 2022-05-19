# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


from django.db import models
from django.contrib.auth.models import User 


#[ ]:upload file to server model

import os
import uuid


from datetime import datetime 

def Firmware_directory_path(instance, filename):
    # Get Current Date
    todays_date = datetime.now()

    path = "uploads/FirmwareFiles/"
    extension = "." + filename.split('.')[-1]


    # Filename reformat
    filename_reformat =  'amir'+ extension

    return os.path.join(path, filename_reformat)



class FirmwareFile(models.Model,):

    file = models.FileField(upload_to='firmware/',null=True)
    name = models.CharField(max_length=255, blank=True)
    # added for delete button action
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    state = models.BooleanField(default=False)
    version = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=255, blank=True)
    docid = models.CharField(max_length=255, blank=True)
    # on_delete = models.restrict : if user deleted from USER table file not be deletted
    owner = models.ForeignKey('auth.User', on_delete=models.RESTRICT, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # def add(request):
    #   file = request.POST['file']
    #   file._name = request.user.id +"."+ file._name.split('.')[1]

    def delete(self, using=None, keep_parents=False):
        self.file.storage.delete(self.file.name)
        super().delete()
    
