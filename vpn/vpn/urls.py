from django.urls import path
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


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-login'),
    path('update-user/', UserUpdateView.as_view(), name='user-update'),
    path('statistics/', StatisticsListView.as_view(), name='statistics-list'),
    path('websites/', WebsiteListView.as_view(), name='website-list'),
    path('websites/<int:pk>/', WebsiteDetailView.as_view(), name='website-detail'),
    path('websites/create/', WebsiteCreateView.as_view(), name='create-website'),
    path('vpn/<path:user_site>/', VPNView.as_view(), name='vpn-view'),
]
