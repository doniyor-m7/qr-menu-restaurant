def language(request):
    return {'lang': request.session.get('lang', 'uz')}
