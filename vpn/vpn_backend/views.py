from rest_framework import generics, permissions, status, serializers
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, StreamingHttpResponse
from vpn_backend.utils import make_proxy_request, replace_internal_links, check_for_vpn_use
from urllib.parse import urlparse
from decimal import Decimal

from .models import User, Website, Statistics
from .serializers import UserSerializer, WebsiteSerializer, StatisticsSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        login(self.request, user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'detail': 'User successfully registered'}, status=status.HTTP_201_CREATED)


class UserLoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=401)
        
        login(request, user)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
        

class UserLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('user-login')


class UserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        if 'password' in serializer.validated_data:
            current_password = serializer.validated_data.pop('password')
            if not self.request.user.check_password(current_password):
                raise serializers.ValidationError({'password': 'Incorrect current password.'})
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'detail': 'User successfully updated'}, status=status.HTTP_200_OK)


class StatisticsListView(generics.ListAPIView):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]


class WebsiteListView(generics.ListCreateAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = [permissions.IsAuthenticated]


class WebsiteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = [permissions.IsAuthenticated]


class WebsiteCreateView(generics.CreateAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        url = serializer.validated_data['url']
        if urlparse(url).scheme:
            url = urlparse(serializer.validated_data['url']).netloc
        existing_website = Website.objects.filter(url=url, user=self.request.user).first()
        if existing_website:
            print('Found website')
            existing_website.name = serializer.validated_data.get('name', existing_website.name)
            existing_website.save()
        else:
            serializer.save(url=url, user=self.request.user)


class VPNView(View):
    def get(self, request, user_site):
        if not request.user.is_authenticated:
            return HttpResponse("User not authenticated", status=401)
        user_site_domain = urlparse(f'https://{user_site}').netloc
        if not check_for_vpn_use(request.user, user_site_domain):
            original_site_url = f'https://{user_site_domain}'
            return redirect(original_site_url)

        website = get_object_or_404(Website, user=request.user, url=user_site_domain)
        return self.process_vpn_request(request, website)

    def process_vpn_request(self, request, website):
        try:
            statistics = Statistics.objects.get(user=request.user, website=website)
            statistics.page_views += 1
        except Statistics.DoesNotExist:
            statistics = Statistics.objects.create(user=request.user, website=website, page_views=1)

        sub_url = (request.path.split(f"/vpn/{website.url}", 1)[-1])[:-1] # [:-1] to remove extra slash 
        original_site_url = f'https://{website.url}{sub_url}'
        proxy_response = make_proxy_request(original_site_url)
        try:
            proxy_response_content = replace_internal_links(proxy_response.content, request.user, website.url, sub_url)
        except AttributeError:
            proxy_response_content = proxy_response

        def streaming_content_generator():
            yield proxy_response_content

        response = StreamingHttpResponse(streaming_content_generator(), content_type='text/html; charset=utf-8')
        
        statistics.data_transferred += Decimal(len(proxy_response_content)) / Decimal(1024 * 1024)
        statistics.save()

        return response
