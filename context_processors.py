def message_processor(request):
    message = request.session.get('message','')
    request.session['message'] = ''
    alert = request.session.get('alert','')
    request.session['alert'] = ''

    message = request.GET.get('message', message)
    alert = request.GET.get('alert', alert)
    return { 'message': message, 'alert' : alert }