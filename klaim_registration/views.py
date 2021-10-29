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
from .models import DataKlaim, ApprovalHRD, DataTK, toQRCode
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
    if request.method == 'POST':
        form = DataTKForm(request.POST, request.FILES)
        if form.is_valid():
            nama = request.POST.get('nama')
            nik = request.POST.get('nik')
            tgl_lahir = request.POST.get('tgl_lahir')
            tempat_lhr = request.POST.get('tempat_lhr')
            alamat = request.POST.get('alamat')
            nama_ibu = request.POST.get('nama_ibu')
            status = request.POST.get('status')
            nama_pasangan = request.POST.get('nama_pasangan')
            tgl_lhr_pasangan = request.POST.get('tgl_lhr_pasangan')
            anak_1 = request.POST.get('anak_1')
            tgl_lhr1 = request.POST.get('tgl_lhr1')
            anak_2 = request.POST.get('anak_2')
            tgl_lhr2 = request.POST.get('tgl_lhr2')
            email = request.POST.get('email')
            no_hp = request.POST.get('no_hp')
            no_rek = request.POST.get('no_rek')
            nama_rek = request.POST.get('nama_rek')

    return render(request, 'klaim_registration/tambah_tk.html')


@login_required(login_url='/accounts/login/')
def TambahTK_ajax(request):
    user = request.user.profile.pk
    # if request.method == 'POST':
    #     form = DataTKForm(request.POST)
    #     if form.is_valid():
    #         form.save()

    #         return redirect(reverse('home-klaim'))
    msg = None
    if request.is_ajax:
        nama = request.POST.get('nama')
        nik = request.POST.get('nik')
        tgl_lahir = request.POST.get('tgl_lahir')
        tempat_lhr = request.POST.get('tempat_lhr')
        alamat = request.POST.get('alamat')
        nama_ibu = request.POST.get('nama_ibu')
        status = request.POST.get('status')
        nama_pasangan = request.POST.get('nama_pasangan')
        tgl_lhr_pasangan = request.POST.get('tgl_lhr_pasangan')
        anak_1 = request.POST.get('anak_1')
        tgl_lhr1 = request.POST.get('tgl_lhr1')
        anak_2 = request.POST.get('anak_2')
        tgl_lhr2 = request.POST.get('tgl_lhr2')
        email = request.POST.get('email')
        no_hp = request.POST.get('no_hp')
        no_rek = request.POST.get('no_rek')
        nama_rek = request.POST.get('nama_rek')
        photo = request.POST.get('photo')
        photo_f = request.POST.get('photo_f')
        ktp = request.POST.get('ktp')
        ktp_f = request.POST.get('ktp_f')
        kk = request.POST.get('kk')
        kk_f = request.POST.get('kk_f')
        paklaring = request.POST.get('paklaring')
        paklaring_f = request.POST.get('paklaring_f')
        # lain = request.POST.get('lain')
        # lain_f = request.POST.get('lain_f')

        DataTK.objects.create(hrd=user, nama=nama, nik=nik, tgl_lahir=tgl_lahir, tempat_lahir=tempat_lhr, alamat=alamat, nama_ibu=nama_ibu,
            status=status, nama_pasangan=nama_pasangan, tgl_lahir_pasangan=tgl_lhr_pasangan, nama_anak_s=anak_1, tgl_lahir_s=tgl_lhr1,
            nama_anak_d=anak_2, tgl_lahir_d=tgl_lhr2, email=email, no_hp=no_hp, nama_rekening=nama_rek, no_rekening=no_rek, propic=photo_f,
            file_ktp=ktp_f, file_kk=kk_f, file_paklaring=paklaring_f, )

        msg = 'Data TK Berhasil di Input!'
        return JsonResponse({'msg':msg})


    return render(request, 'klaim_registration/tambah_tk.html')
