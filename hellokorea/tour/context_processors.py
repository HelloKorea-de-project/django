from django.conf import settings

def api_keys(request):
    return {
        'NAVER_MAPS_API_KEY': settings.NAVER_MAPS_API_KEY,
    }