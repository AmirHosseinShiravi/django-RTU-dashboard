import psutil
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime, timedelta
# Create your views here.


@login_required(login_url="/login/")
def systemStatus(request):
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())

    context ={'cpu_usage': psutil.cpu_percent(1),
              'ram_usage': psutil.virtual_memory().percent,
              'disk_total': '{0:4.2f}'.format(psutil.disk_usage('/').total/ 1024**3),
              'disk_used': '{0:4.2f}'.format(psutil.disk_usage('/').used / 1024**3),
              'disk_used_percent': psutil.disk_usage('/').percent,
              'disk_free': '{0:4.2f}'.format(psutil.disk_usage('/').free / 1024**3),
              'disk_free_percent': psutil.disk_usage('/'),
              'datetime': datetime.now(),
              'uptime': f'{uptime.days} days, {uptime.seconds // 3600} hours, {(uptime.seconds // 60) % 60} minutes, {uptime.seconds % 60} seconds'
              }
    return JsonResponse(context)
