#!/usr/bin/env python
import os
import sys
import django
import hashlib
from bs4 import BeautifulSoup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secmon.settings')
django.setup()
from model.models import devassets, portssets

def main():
    parse_xml(r'c:\stduio\downloads\scanrs.xml')

def genid(input):
    sh  =  hashlib.sha256()
    sh.update(input.encode())
    return sh.hexdigest()
def parse_xml(xml_filename):
    soup = BeautifulSoup(open(xml_filename,'r').read(),'lxml')
     #遍历所有的host标签
    for host in soup.find_all('host'):
    #找到存活的主机
        if host.status['state'] == 'up':
        #主机的IP地址
            devdic = {}
            addrs = host.find_all('address')
            for addr in addrs:
                if addr['addrtype'] == 'ipv4':
                    devdic['ip'] = addr['addr']
                if addr['addrtype'] == 'mac':
                    devdic['mac'] = addr['addr']
                    devdic['vendor'] = addr['vendor']
            if host.hostnames.hostname is not None:
                devdic['hostname'] = host.hostnames.hostname['name']
            if devdic.get('mac') is None:
                devdic['mac'] ='00:00:00:00:00:00'
            devdic['aid'] =genid(devdic['mac'])
            devset = None
            try:
                devset = devassets.objects.get(aid = devdic['aid'] )
            except Exception as e:
                print(type(e))
                pass
            if devset is None:
                 devset = devassets()
                 devset.aid = devdic['aid']
            devset.ip = devdic['ip']
            if devdic.get('hostname') is not None:
                devset.hostname = devdic['hostname']
            devset.mac = devdic['mac'] 
            if devdic.get('vendor') is not None:
                devset.vendor = devdic['vendor']
            devset.save()
            for port in host.ports.find_all('port'):
                portset = None
                try:
                    portset = portssets.objects.get(devasset=devset, port = int(port['portid']))
                except Exception as e:
                    print(type(e))
                if portset is None:
                    portset = portssets()
                    portset.devasset = devset
                portset.port = int(port['portid'])
                portset.srvname = port.service['name']
                if port.service.get('product') is not None:
                    portset.product = port.service['product']
                portset.protocol = port['protocol']
                portset.state = port.state['state']
                if port.service.get('ostype') is not None:
                    portset.ostype = port.service['ostype']
                if port.service.get('extrainfo') is not None:
                    portset.extrainfo = port.service['extrainfo']
                portset.save()
            

if __name__ == '__main__':
    main()
