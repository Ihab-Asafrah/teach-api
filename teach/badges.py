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


header = {"X-Api-Key": "0a15419a6dd7bdca91a24aa536457e3d", 
          "X-Api-Secret": "rMs8RVcwfPDEyNdeRPpmUfeBhu4dDZvLVSHBxhWU7vQhIIMO38xPkYLXD2n+vU5l7zywcXs0D5Uy4XvWYE3Fbt0XK5zbVCLxzWl6+uNsVXpHI+NToAkZZy1Q2C+D5Oh72/OjyWq9U7soHgbYhNCgebblziLhzexIk+OB0y1axH4="}

username = "abualkarmi@gmail.com"
password = "123123"
token = "94eaf1ee16672d422a5c24aa94756064c86e85618a5ca5aa171c1d29995cb527ebebe561ddc9d7e7dc59c59191bb8648341dc0c3f05b216d49c177bb47c37261"



@require_GET
@csrf_exempt
def authenticate(request):
    url = "https://api.credly.com/v1.1/authenticate"
    credentials = HTTPBasicAuth(username, password)
    response = requests.post(url, auth=credentials, headers=header)
    
    return HttpResponse(response.content)



@require_GET
def findBadges(request):
    url = "https://api.credly.com/v1.1/me/badges/created?access_token=" + token + "&page=1&per_page=10&order_direction=ASC"
    response = requests.get(url, headers=header)
    
    return HttpResponse(response.content) #CCCCCCC
    
    



