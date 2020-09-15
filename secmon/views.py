from django.http import HttpResponse
from django.shortcuts import render
from model.models import devassets, portssets
def showtable(request):
    context = {}
    ipassets = devassets.objects.all()
    context['hello'] = 'Hello World!'
    context['ipassets'] = ipassets
    return render(request, 'showtable.html', context)

def portdetail(request):
    context = {}
    ports = None
    id = request.GET.get('id')
    #portinfo = portssets.objects.get(id=int(id))
    devid = request.GET.get('assetid')
    if devid is not None and int(devid) > -1:
        mydevset = devassets.objects.get(id=int(devid))
        context['ip'] = mydevset.ip
        ports = mydevset.portdev.all()
    elif id is not None:
        ports = portssets.objects.filter(id=int(id))
        for port in ports:
            context['ip'] = port.devasset.ip
            break
    context['ports'] = ports
    return render(request, 'portinfo.html', context)