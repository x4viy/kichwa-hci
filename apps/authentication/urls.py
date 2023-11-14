# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path,include
from .views import login_view, register_user , logout_view, PersonalizedPasswordResetView,PersonalizedPasswordResetDoneView,PersonalizedPasswordResetConfirmView, PersonalizedPasswordResetCompleteView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", logout_view, name="logout"),
    path('personalized_password_reset/', PersonalizedPasswordResetView.as_view(), name='password_reset'),
    path('personalized_password_reset/done/', PersonalizedPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('personalized_reset/<uidb64>/<token>/', PersonalizedPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('personalized_reset/done/', PersonalizedPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


