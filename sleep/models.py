# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class SleepUser(models.Model):
    id = models.CharField(verbose_name='学号',max_length=13,primary_key=True)
    password = models.CharField(verbose_name='密码',max_length=30)
    startTime = models.TimeField(verbose_name='睡觉开始时间')
    endTime = models.TimeField(verbose_name='睡觉结束时间')
    def __unicode__(self):
        return u"%s ===> %s-%s" % (self.id,self.startTime,self.endTime)
