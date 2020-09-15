from django.db import models

# Create your models here.
class devassets(models.Model):
    aid = models.CharField(max_length=80)
    hostname = models.CharField(max_length=32,null=True)
    ip = models.CharField(max_length=32)
    mac = models.CharField(max_length=32)
    vendor = models.CharField(max_length=64,null=True)
    
    @property
    def all_ports(self):
        return self.portdev.all()

class portssets(models.Model):
    devasset = models.ForeignKey(devassets, related_name='portdev',on_delete=models.CASCADE)
    #aid = models.CharField(max_length=20)
    port = models.IntegerField()
    protocol = models.CharField(max_length=8,db_index=True)
    srvname = models.CharField(max_length=64,null=True)
    product =  models.CharField(max_length=120,null=True)
    ostype =  models.CharField(max_length=64,null=True)
    state = models.CharField(max_length=8)
    extrainfo = models.CharField(max_length=128,null=True)
