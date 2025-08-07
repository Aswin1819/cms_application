from django.conf import settings

def set_jwt_cookies(response, access_token, refresh_token):
    response.set_cookie(
        key='access',
        value=access_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        max_age=3600,
        path='/',
    )
    response.set_cookie(
        key='refresh',
        value=refresh_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        max_age=3600,
        path='/',
    )
    return response