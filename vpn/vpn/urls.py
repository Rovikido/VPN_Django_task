from django.urls import path
from django.contrib import admin
from vpn_backend.views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserUpdateView,
    StatisticsListView,
    WebsiteListView,
    WebsiteDetailView,
    WebsiteCreateView,
    VPNView,
)
from vpn_backend.views_alternative import *


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/register/', UserRegistrationView.as_view(), name='api-user-register'),
    # path('api/login/', UserLoginView.as_view(), name='api-user-login'),
    # path('api/logout/', UserLogoutView.as_view(), name='api-user-logout'),
    # path('api/update-user/', UserUpdateView.as_view(), name='api-user-update'),
    # path('api/statistics/', StatisticsListView.as_view(), name='api-statistics-list'),
    # path('api/websites/', WebsiteListView.as_view(), name='api-website-list'),
    # path('api/websites/<int:pk>/', WebsiteDetailView.as_view(), name='api-website-detail'),
    # path('api/websites/create/', WebsiteCreateView.as_view(), name='api-create-website'),
    path('vpn/<path:user_site>/', VPNView.as_view(), name='vpn-view'),

    path('register/', UserRegistrationViewAlternative.as_view(), name='user-register'),
    path('login/', UserLoginViewAlternative.as_view(), name='user-login'),
    path('logout/', UserLogoutViewAlternative.as_view(), name='user-logout'),
    path('update-user/', UserUpdateViewAlternative.as_view(), name='user-update'),
    path('statistics/', StatisticsListViewAlternative.as_view(), name='statistics-list'),
    path('websites/', WebsiteListViewAlternative.as_view(), name='website-list'),
    path('websites/<int:pk>/', WebsiteDetailViewAlternative.as_view(), name='website-detail'),
    path('websites/create/', WebsiteCreateViewAlternative.as_view(), name='create-website'),
    path('', WebsiteListViewAlternative.as_view(), name='home'),
]
