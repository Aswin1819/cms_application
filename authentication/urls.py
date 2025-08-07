from django.urls import path
from . views import *

urlpatterns = [
    path('register/',RegisterUserView.as_view(), name='register'),
    path('login/',LoginUserView.as_view(), name='token_obtain_pair'),
    path('token/refresh',CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LoginUserView.as_view(), name='logout'),
    path('profile/',UserProfileView.as_view(), name='user-profile'),
    
    
    
    
]
