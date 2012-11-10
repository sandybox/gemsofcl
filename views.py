from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import redirect

from craigslist.models import Item, ItemImage

def home(request):
    c = RequestContext(request, {}, [])
    return render_to_response('index.html', c)

def play(request):
    item = Items.objects.filter(active=True).order_by('?')[1]

    c = RequestContext(request, {'item':item}, [])
    return render_to_response('play.html', c)