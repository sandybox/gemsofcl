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

    c = RequestContext(request, {'item':item}, [])
    return render_to_response('play.html', c)