# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework import permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from .serializer import PerusahaanSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse

from authentication.models import Perusahaan, Profile
from .forms import LoginForm, SignUpForm, ProfileForm


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/page-login.html", {"form": form, "msg": msg})


def register_user(request):

    return render(request, "accounts/page-register.html")


def register_user_ajax(request):
    msg = None
    if request.is_ajax():
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        npp_id = request.POST.get('no_npp')

        if password1 != password2:
            msg = 'Password Tidak Sama!'
        else:
            password = make_password(password1, salt=['username'])
            User.objects.update_or_create(
                username=username, password=password, email=email, is_active=False)
            user = User.objects.get(username=username)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('authentication/acc_activate_email.html', {
                'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user), })
            to_mail = EmailMessage(mail_subject, message, to=[email])
            to_mail.send()
            try:
                Profile.objects.update_or_create(
                    user__username=username, defaults={'npp_id': npp_id})
            except:
                pass
            msg = 'Please confirm your email address to complete the registration '
            response = {
                'msg': msg
            }
            return JsonResponse(response)


def activate_email(request, uidb64, token):
    msg = None
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        profile = Profile.objects.get(user__id=user.pk)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        profile.is_hrd = True
        profile.save()
        msg = 'Akun sudah aktif. Silahkan login di <a href="/accounts/login/">sini</a>'
        return HttpResponse(msg)
    else:
        return HttpResponse('Akctivation link is invalid!')


@login_required(login_url='/accounts/login/')
def settingProfile(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
                           instance=request.user.profile)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "accounts/profile.html", {'form': form})


@login_required(login_url='/accounts/login/')
def DetilProfile(request):
    # pk = request.user.profile.id
    qs = Profile.objects.select_related(
        'user').filter(user__username=request.user)
    context = {
        'datas': qs
    }
    return render(request, 'authentication/profile.html', context)


class ListPerusahaan(ListCreateAPIView):
    serializer_class = PerusahaanSerializer
    permission_classes = [permissions.AllowAny, ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['npp', ]
    search_fields = ['npp', ]

    def get_queryset(self):

        qs = Perusahaan.objects.all()
        if qs.exists():
            return qs
        else:
            return qs.none
