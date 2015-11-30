'''
Created on Nov 24, 2015

@author: Ihab Asafrah
@organization: Souktel Digital Solutions
@contact: ihab@souktel.org
'''

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import requests
from requests.auth import HTTPBasicAuth

from views import check_origin
from views import json_response



CREDLY_APP_API_KEY="b22824fd98b0c98cebcd828fcc060949"
CREDLY_APP_SECRET_KEY="XsfOH17tBtDEGB7iJ6UMBwApd45n0SOHz/hXqb2XXJ6FIqDt1ppBBNt9bM0xAdCI1r0CtjZ8fjHMC3krdw0bPQhHzOzhq4U3RYYGDG2n5dad1hltc/nc8OKsPCk65CW+gMCoxht8E0bdLm6A1nYOJlyrDCJhYRwwhBgy1GxvbLM="


header = {"X-Api-Key": CREDLY_APP_API_KEY,"X-Api-Secret": CREDLY_APP_SECRET_KEY}


DEFAULT_PAGE_NUM = 1
BADGES_PER_PAGE = 10
DEFAULT_ORDER = "ASC"
BADGES_API_URL = 'https://apistaging.credly.com/v1.1'
token='2fa1b38ac37a45a3d5e59fd5c3046124361f958221ea276d11ff34b4ebd29f9a7eaf0d6573c837457af13eee943a71cfeb4324041e73b68c6e65174c42ad0ecf'

@require_POST
@csrf_exempt
def authenticate(request):
    # @todo
    # please check this before the production

    res = check_origin(request)
    if res is None:
        return HttpResponse('invalid origin', status=403)
    res['access-control-allow-credentials'] = 'true'

    url = BADGES_API_URL + "/authenticate"
    credentials = HTTPBasicAuth(request.POST.get('username'), request.POST.get('password'))

    response = requests.post(url, auth=credentials, headers=header)
    return json_response(res, json.JSONDecoder().decode(response.content))

@require_GET
def findBadges(request):
    # @todo
    # please check this before the production

    res = check_origin(request)
    if res is None:
        return HttpResponse('invalid origin', status=403)
    res['access-control-allow-credentials'] = 'true'

    query = request.GET.get("search", "")
    memberId = int(request.GET.get("userId", 0))
    showDetails = request.GET.get("details", False)
    pageNum = int(request.GET.get("page", DEFAULT_PAGE_NUM))
    badgesPerPage = int(request.GET.get("size", BADGES_PER_PAGE))
    orderDirection = request.GET.get("direction", DEFAULT_ORDER)

    url = "/badges?query=%s&member_id=%dverbose=%d&page=%d&per_page=%d&order_direction=%s&access_token=%s" % (query, memberId, showDetails, pageNum, badgesPerPage, orderDirection, token)
    url = BADGES_API_URL + url
    response = requests.get(url, headers=header)

    return json_response(res,json.JSONDecoder().decode(response.content))

