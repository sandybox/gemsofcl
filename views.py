from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.conf import settings

def home(request):
    c = RequestContext(request, {}, [])
    return render_to_response('index.html',
        {'base_site_url' : settings.BASE_SITE_URL,
        'base_site_url_s' : settings.BASE_SITE_URL_S,}, c)

def play(request):
    c = RequestContext(request, {}, [])
    return render_to_response('play.html', c)

def about(request):
    c = RequestContext(request, {}, [])
    return render_to_response('about.html', c)