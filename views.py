from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.conf import settings

from craigslist.models import Item, ItemImage

def home(request):
    c = RequestContext(request, {}, [])
    return render_to_response('index.html',
        {'base_site_url' : settings.BASE_SITE_URL,
        'base_site_url_s' : settings.BASE_SITE_URL_S,}, c)

def play(request):
    # Check if this was a vote and track it
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action  = request.POST.get('action')
        try:
            item_id = int(item_id)
            item = Item.objects.get(id=item_id)
            item.num_views += 1
            if action.lower() == 'gem':
                item.num_likes += 1
            elif action.lower() == 'dud':
                item.num_dislikes += 1
            else:
                raise Exception('No such action!')
            item.save()
        except Exception, e:
            print 'Could note vote: %s' % str(e)

    item = Item.objects.filter(active=True,price__isnull=False).order_by('?')[1]
    countdown = 10 # NEED TO REPLACE TO VAR STORED IN SESSION
    c = RequestContext(request, {'item':item, 'countdown':countdown, }, [])
    return render_to_response('play.html', c)

def about(request):
    c = RequestContext(request, {}, [])
    return render_to_response('about.html', c)

def displaygems(request):
    c = RequestContext(request, {}, [])
    return render_to_response('displaygems.html', c)
