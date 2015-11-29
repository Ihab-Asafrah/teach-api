'''
Created on Nov 24, 2015

@author: Ihab Asafrah
@organization: Souktel Digital Solutions
@contact: ihab@souktel.org
'''

import json
import urlparse
import django.contrib.auth
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.utils.crypto import get_random_string
import django_browserid.base
import requests
from rest_framework import routers
from rest_framework.authtoken.models import Token
from . import webmaker, new_webmaker
from .new_webmaker import get_idapi_url
import httplib, urllib
from requests.auth import HTTPBasicAuth
from django.views.decorators.csrf import requires_csrf_token 
from mmap import PAGESIZE


header = {"X-Api-Key": "b22824fd98b0c98cebcd828fcc060949", 
          "X-Api-Secret": "XsfOH17tBtDEGB7iJ6UMBwApd45n0SOHz/hXqb2XXJ6FIqDt1ppBBNt9bM0xAdCI1r0CtjZ8fjHMC3krdw0bPQhHzOzhq4U3RYYGDG2n5dad1hltc/nc8OKsPCk65CW+gMCoxht8E0bdLm6A1nYOJlyrDCJhYRwwhBgy1GxvbLM="}

username = "mozilla@credly.com"
password = "V9tuTUgy"
token = "6685a1a0022cb8219ecb1305de6f83f804e6ba0d047fc595d3abb811fbcb647f504c7fcd74cd8efe69f31a78bd72294a136c0ed573ca6dc68a7a42473c5b0d18"

DEFAULT_PAGE_NUM = 1
BADGES_PER_PAGE = 10
DEFAULT_ORDER = "ASC"


@require_GET
@csrf_exempt
def authenticate(request):
    url = "https://apistaging.credly.com/v1.1/authenticate"
    credentials = HTTPBasicAuth(username, password)
    response = requests.post(url, auth=credentials, headers=header)
    
    return HttpResponse(response.content)



@require_GET
def findBadges(request):
    query = request.GET.get("search", "")
    memberId = int(request.GET.get("userId", 0))
    showDetails = request.GET.get("details", False)
    pageNum = int(request.GET.get("page", DEFAULT_PAGE_NUM))
    badgesPerPage = int(request.GET.get("size", BADGES_PER_PAGE))
    orderDirection = request.GET.get("direction", DEFAULT_ORDER)
    
    url = "https://apistaging.credly.com/v1.1/badges?query=%s&member_id=%dverbose=%d&page=%d&per_page=%d&order_direction=%s&access_token=%s" % (query, memberId, showDetails, pageNum, badgesPerPage, orderDirection, token)
    response = requests.get(url, headers=header)
    
    return HttpResponse(response.content)    

