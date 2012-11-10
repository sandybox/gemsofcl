from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.conf import settings

from django.core.mail import send_mail

from craigslist.models import Item, ItemImage, Subscriber

import logging
logger = logging.getLogger(__name__)

def home(request):
    if 'countdown' not in request.session:
        request.session['countdown'] = settings.COUNTDOWN_START

    c = RequestContext(request, {}, [])
    return render_to_response('index.html', {}, c)

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
            logger.error('Could note vote: %s' % str(e))

        if 'countdown' in request.session:
            request.session['countdown'] = request.session['countdown'] - 1 # NEED TO REPLACE TO VAR STORED IN SESSION
            logger.debug("%s hello" % (request.session['countdown']))
            if request.session['countdown'] == 0:
                request.session['message'] = 'Congratulations! You can now check out the Gems of Craigslist'
                return redirect('displaygems')
        else:
            request.session['countdown'] = settings.COUNTDOWN_START
            logger.debug("starting countdown at %d" % settings.COUNTDOWN_START)

    if 'countdown' not in request.session:
        request.session['countdown'] = settings.COUNTDOWN_START

    try:
        item = Item.objects.filter(active=True,price__isnull=False).order_by('?')[1]
    except Exception, e:
        logger.error('Could not get item: %s' % str(e))
        item = None
        request.session['alert'] = 'Sorry! We\'ve run out of items!'

    c = RequestContext(request, {'item':item,}, [])
    return render_to_response('play.html', c)

def about(request):
    c = RequestContext(request, {}, [])
    return render_to_response('about.html', c)

def displaygems(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            if '@' in email and '.' in email:
                subscriber = Subscriber(email=email.lower())
                subscriber.save()
                request.session['message'] = 'Thanks for signing up!'

                # Send welcome email
                send_mail('Welcome to the Gems of Craigslist', 'We\'ll email you the best Craigslist items daily.', 'Gems of Craigslist <team@gemsofcl.com>',
                    [email.lower()], fail_silently=True)

            else:
                request.session['alert'] = 'Please enter a valid email address.'
        except Exception, e:
            request.session['alert'] = 'Sorry. We were not able to sign you up. Please try again.'

    items = Item.objects.filter(active=True,price__isnull=False,num_views__gt=0,num_likes__gt=0).extra(select={ 'rating' : 'num_likes / num_views' }).order_by('-rating')[:10]
    c = RequestContext(request, {'items':items}, [])

    return render_to_response('displaygems.html', c)
