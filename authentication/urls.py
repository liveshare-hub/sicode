# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from .views import login_view, register_user, settingProfile, register_user_ajax, activate_email, ListPerusahaan
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    # path('register/', register_user, name="register"),
    path('register/', register_user, name="register"),
    path('register/ajax', register_user_ajax, name="create-user"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,64})/$', activate_email, name='activate'),
    path('api/perusahaan', ListPerusahaan.as_view(), name='api-perusahaan'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", settingProfile, name="profile")
]
