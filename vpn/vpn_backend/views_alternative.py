from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, get_user_model, update_session_auth_hash
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Statistics, Website
from urllib.parse import urlparse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username'] 


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class WebsiteCreateForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = [ 'name', 'url']

    def save(self, commit=True):
        user = self.request.user
        self.instance.user = user
        return super().save(commit)


class UserLoginViewAlternative(View):
    template_name = 'login.html'
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(request, 'login_success.html', {'user': user})
        else:
            return render(request, self.template_name, {'form': form, 'error_message': 'Invalid credentials'})

    def get(self, request, *args, **kwargs):
        form = self.form_class(request)
        return render(request, self.template_name, {'form': form, 'user': request.user})


class UserRegistrationViewAlternative(CreateView):
    model = get_user_model()
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_template_name = 'registration_success.html'

    def form_valid(self, form):
        super().form_valid(form)
        user = form.save()
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        login(self.request, user)
        return render(self.request, self.success_template_name, {'user': user})
    
    def get_success_url(self):
        return reverse_lazy('website-list')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if username and get_user_model().objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')

        if email and get_user_model().objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = False
        self.fields['password'].required = True
        self.fields['password'].widget = forms.PasswordInput(render_value=False)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if username and get_user_model().objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')

        if email and get_user_model().objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')

        return cleaned_data

class UserUpdateViewAlternative(LoginRequiredMixin, View):
    template_name = 'update_user.html'
    success_template_name = 'update_success.html'

    def get(self, request, *args, **kwargs):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form, 'user': request.user})

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.cleaned_data.pop('password', None)
            form.save()
            messages.success(request, 'User successfully updated.')
            return render(request, self.success_template_name, {'user': request.user})

        return render(request, self.template_name, {'form': form, 'user': request.user})


class UserLogoutViewAlternative(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/login')


class StatisticsListViewAlternative(LoginRequiredMixin, View):
    template_name = 'statistics_list.html'

    def get(self, request, *args, **kwargs):
        statistics = Statistics.objects.filter(user=request.user)
        return render(request, self.template_name, {'statistics': statistics, 'user': request.user})


class WebsiteListViewAlternative(LoginRequiredMixin, View):
    template_name = 'website_list.html'

    def get(self, request, *args, **kwargs):
        websites = Website.objects.filter(user=request.user)
        return render(request, self.template_name, {'websites': websites, 'user': request.user})


class WebsiteDetailViewAlternative(LoginRequiredMixin, View):
    template_name = 'website_detail.html'

    def get(self, request, pk, *args, **kwargs):
        website = Website.objects.get(pk=pk, user=request.user)
        return render(request, self.template_name, {'website': website, 'user': request.user})


class WebsiteCreateViewAlternative(LoginRequiredMixin, CreateView):
    model = Website
    template_name = 'create_website.html'
    form_class = WebsiteCreateForm
    success_template_name = 'create_website_success.html'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.request = self.request
        return form

    def form_valid(self, form):
        url = form.cleaned_data['url']
        if urlparse(url).scheme:
            url = urlparse(url).netloc
        existing_website = Website.objects.filter(url=url, user=self.request.user).first()
        if existing_website:
            existing_website.name = form.cleaned_data.get('name', existing_website.name)
            existing_website.save()
        else:
            form.instance.url = url
            form.instance.user = self.request.user
            form.save()
            Statistics.objects.create(user=self.request.user, website=form.instance)
        return render(self.request, self.success_template_name, {'user': self.request.user})
