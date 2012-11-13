from django.conf import settings

def message_processor(request):
    message = request.session.get('message','')
    request.session['message'] = ''
    alert = request.session.get('alert','')
    request.session['alert'] = ''

    message = request.GET.get('message', message)
    alert = request.GET.get('alert', alert)
    return { 'message': message, 'alert' : alert }

def include_google_analytics(request):
    return { 'include_ga': settings.INCLUDE_GA }

def template_debug(request):
    return { 'debug_on' : settings.ENV_DEV }