from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import redirect

def home(request):
    c = RequestContext(request, {}, [])
    return render_to_response('index.html', c)