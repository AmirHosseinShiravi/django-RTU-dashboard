# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from distutils.command.upload import upload
from distutils.log import error
import sys, os
import uuid
from django import template
from django.contrib.auth.decorators import login_required, permission_required
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
#[+]: upload file to server header modules
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import FirmwareFile
from django.shortcuts import render, redirect
from datetime import datetime
from core.settings import MEDIA_ROOT
##########################################

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/home.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    # try:

    load_template = request.path.split('/')[-1]

    if load_template == 'admin':
        return HttpResponseRedirect(reverse('admin:index'))
    context['segment'] = load_template

    html_template = loader.get_template('home/' + load_template)
    return HttpResponse(html_template.render(context, request))

    # except template.TemplateDoesNotExist:

    #     html_template = loader.get_template('home/page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))




#[+]: send system datetime to requests from pages
from time import time
from django.http import JsonResponse

@login_required(login_url="/login/")
def get_time(request):
    system_time = int(time() * 1000) # js unix timestamp is based on milisecond
    return JsonResponse({"system_time": system_time})




#[+]: upload file to server 
#[-]: add progress bar to frontend
#[-]: show directory files in frontend
#[-]: delete, download, select file 
#[-]: add permission and group permission to access this ability's
#[-]: complete Document Model fields
@login_required(login_url='/login/')
def FirmewareManagement(request):
    msg = ''
    if request.method == 'POST' and request.FILES:
        if request.user.has_perm('home.add_firmwarefile'):
            form = UploadFileForm(request.POST, request.FILES)
            print(form.data)
            if form.is_valid():
                form.save()

                last_firmware_uploaded = FirmwareFile.objects.latest('id')
                # [+]: add file size
                file_size = int(request.META['CONTENT_LENGTH'])
                if file_size:
                    if(file_size < 1024):
                        last_firmware_uploaded.size = str(file_size) + ' ' + 'Bytes'
                    elif (1024 <= file_size < 1024 ** 2):
                        last_firmware_uploaded.size = '{0:.2f}'.format(file_size / 1024 ) + ' ' + 'KB'
                    elif (1024 ** 2 <= file_size):
                        last_firmware_uploaded.size = '{0:.2f}'.format(file_size / 1024 ** 2) + ' ' + 'MB'
                    
                # [+]: add file uploader user
                last_firmware_uploaded.owner =  request.user             
                # [-]: open file and read file version and DocID
                with open(last_firmware_uploaded.file.path ) as f:
                    pass
        
                last_firmware_uploaded.save()
                msg = 'successfully file uploaded'
        else:
            msg = 'you have no permission to upload file'

    elif request.method == 'GET' and 'deletefile' in request.GET:
        if request.user.has_perm('home.delete_firmwarefile'):
            must_deleted_query = FirmwareFile.objects.get(uuid= request.GET['deletefile'])
            if must_deleted_query.state == True:
                msg = 'please select another firmware before delete this file'
            else:
                must_deleted_query.delete()
                msg = 'successfully file deleted'
        else:
            msg = 'you have no permission to delete file'
            






    elif request.method == 'GET' and 'downloadfile' in request.GET:
        if request.user.has_perm('home.view_firmwarefile'):
            must_downloaded_query= FirmwareFile.objects.get(uuid= request.GET['downloadfile'])
            if os.path.exists(must_downloaded_query.file.path ) :
                # let FileResponse open file by itself 
                response = FileResponse(open(must_downloaded_query.file.path , 'rb' ) ) 
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(must_downloaded_query.file.name)
                return response
        else:
            msg = 'you have no permission to download file'

    elif request.method == 'GET' and 'selected_firmwareuuid' in request.GET:

        if request.user.has_perm('home.change_firmwarefile'):
            #[+]: now we have to check if there is any other selected file
            selected_firmwareuuid = request.GET['selected_firmwareuuid']

            firmware_list = FirmwareFile.objects.all()
            for firmware in firmware_list:
                if str(firmware.uuid) == str(selected_firmwareuuid):
                    firmware.state = True
                else:
                    firmware.state = False
                firmware.save()
     
            #[-]: now we have to apply firmware file instruction


            msg = 'successfully selected file'
        else:
            msg = 'you have no permission to select file'
    
    elif request.method == 'GET' and 'apply-last-uploaded-firmware' in request.GET:
        if request.user.has_perm(('home.change_firmwarefile')) and request.user.has_perm('home.add_firmwarefile'):
            
            selected_firmwareuuid = request.GET['apply-last-uploaded-firmware']
            firmware_list = FirmwareFile.objects.all()
            for firmware in firmware_list:
                if str(firmware.uuid) == str(selected_firmwareuuid):
                    firmware.state = True
                else:
                    firmware.state = False
                firmware.save()
            
            msg = 'successfully applied last uploaded firmware'

            
        else:
            msg = 'you have no permission to apply firmware file'

    else:
        pass
        
    form = UploadFileForm()
    # data = FirmwareFile(version= 'ewewewe',state='Active', docid='fdfdfdf',size='156545400',file='/Firefox_Screenshot_2022-05-11T04-10-14.899Z.png')
    # data.save()

    firmware_list = FirmwareFile.objects.all().order_by('-uploaded_at')
    # firmware_list.delete()

    context={'form': form ,
             'Firmware_list': firmware_list,
             'msg' : msg
            }
    html_template = loader.get_template("home/Management/Firmware-Management.html")
    return HttpResponse(html_template.render(context, request))



@login_required(login_url='/login/')
def change_firmware_action(request):
    context={}
    print(request.POST)
    return JsonResponse({"system_time": context})