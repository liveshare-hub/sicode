from django.http.response import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.db.models import Subquery, OuterRef, IntegerField
from django.http import JsonResponse
# from dal import autocomplete
import random
import string

from django.core import serializers

from .form import DataTKForm
from .models import DataKlaim, ApprovalHRD, toQRCode
from authentication.models import Perusahaan, Profile
from .decorators import admin_only

from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.conf import settings

from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from django.utils.html import strip_tags
from email.mime.base import MIMEBase
from email import encoders


@login_required(login_url='/accounts/login/')
def index(request):

    return HttpResponse('Ini Rumah')


@login_required(login_url='/accounts/login/')
def TambahTK(request):
    # user = request.user.profile.pk
    # if request.method == 'POST':
    #     form = DataTKForm(request.POST)
    #     if form.is_valid():
    #         form.save()

    #         return redirect(reverse('home-klaim'))
    if request.is_ajax():
        nama = request.POST.get('nama')
        nik = request.POST.get('nik')
        tgl_lahir = request.POST.get('tgl_lahir')
        tempat_lhr = request.POST.get('tempat_lhr')

    return render(request, 'klaim_registration/tambah_tk.html')
