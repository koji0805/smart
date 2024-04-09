from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView, View
from .forms import RegistForm, UserLoginForm, UserUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()  # カスタムユーザーモデルを取得

class HomeView(TemplateView):
    template_name = 'home.html'

class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    model = User  # カスタムユーザーモデルを設定

class UserLoginView(LoginView):
    template_name = 'user_login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        remember = form.cleaned_data['remember']
        if remember:
            self.request.session.set_expiry(1200000)
        return super().form_valid(form)

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:user_login')

class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User  # カスタムユーザーモデルを設定
    form_class = UserUpdateForm
    template_name = 'user_update.html'
    success_url = reverse_lazy('food:list_foods')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        # form.saveメソッドにrequestオブジェクトを渡す
        form.save(request=self.request)
        return super().form_valid(form)
