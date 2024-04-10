from django.urls import path
from django.views.generic.base import RedirectView
from .views import (
    RegistUserView, HomeView, UserLoginView,
    UserLogoutView, UserView, UserUpdateView
)

urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/home/'), name='root_redirect'),
    path('accounts/home/', HomeView.as_view(), name='home'),
    path('accounts/regist/', RegistUserView.as_view(), name='regist'),
    path('accounts/user_login/', UserLoginView.as_view(), name='user_login'),
    path('accounts/user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('accounts/user/', UserView.as_view(), name='user'),
    path('accounts/edit_profile/', UserUpdateView.as_view(), name='edit_profile'),
]
