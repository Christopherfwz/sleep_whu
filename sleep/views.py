# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from .tasks import checkWhetherSleep

def index(request):
    checkWhetherSleep.delay()
    return HttpResponse("OK!")