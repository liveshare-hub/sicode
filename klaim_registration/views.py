from django.contrib.messages.api import success
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
# from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.db.models import Subquery, OuterRef, IntegerField
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
# from dal import autocomplete
import random
import string

from django.core import serializers
from django.views.generic.list import ListView

from .form import DataTKForm, KPJForm, KlaimForm, KpjInlineFormset
from .models import KPJ, DataKlaim, ApprovalHRD, DataTK, SebabKlaim, toQRCode
from authentication.models import Perusahaan, Profile
# from .decorators import admin_only

from django.core.mail import EmailMessage, EmailMultiAlternatives

# from django.conf import settings

from django.template.loader import render_to_string
from email.mime.image import MIMEImage
# from django.utils.html import strip_tags
from email.mime.base import MIMEBase
from email import encoders


@login_required(login_url='/accounts/login/')
def index(request):

    datas = DataTK.objects.select_related('hrd').filter(hrd=request.user.profile).annotate(data_kpj=Subquery(KPJ.objects.filter(
        data_tk=OuterRef('pk'), is_aktif=True).values('no_kpj')))

    # datas = DataTK.objects.select_related('hrd').filter(hrd=request.user.profile).all()
    context = {
        'datas': datas
    }
    return render(request, 'klaim_registration/index.html', context)


@login_required(login_url='/accounts/login/')
def TambahTK(request):
    if request.method == 'POST':
        form = DataTKForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.hrd = request.user.profile
            post.nama = form.cleaned_data['nama']
            post.nik = form.cleaned_data['nik']
            post.tgl_lahir = form.cleaned_data['tgl_lahir']
            post.tempat_lhr = form.cleaned_data['tempat_lahir']
            post.alamat = form.cleaned_data['alamat']
            post.nama_ibu = form.cleaned_data['nama_ibu']
            post.status = form.cleaned_data['status']
            post.nama_pasangan = form.cleaned_data['nama_pasangan']
            post.tgl_lhr_pasangan = form.cleaned_data['tgl_lahir_pasangan']
            post.anak_1 = form.cleaned_data['nama_anak_s']
            post.tgl_lhr1 = form.cleaned_data['tgl_lahir_s']
            post.anak_2 = form.cleaned_data['nama_anak_d']
            post.tgl_lhr2 = form.cleaned_data['tgl_lahir_d']
            post.email = form.cleaned_data['email']
            post.no_hp = form.cleaned_data['no_hp']
            post.no_rek = form.cleaned_data['no_rekening']
            post.nama_rek = form.cleaned_data['nama_rekening']
            post.propic = form.cleaned_data['propic']
            post.file_kk = form.cleaned_data['file_kk']
            post.file_ktp = form.cleaned_data['file_ktp']
            post.file_paklaring = form.cleaned_data['file_paklaring']
            post.file_lain = form.cleaned_data['file_lain']
            post.save()

            return redirect('home-klaim')
    else:
        form = DataTKForm()

    return render(request, 'klaim_registration/tambah_tk.html', {'form': form})


@login_required(login_url='/accounts/login/')
def tambah_kpj(request, pk):
    id_tk = DataTK.objects.get(pk=pk)
    if request.method == 'POST':
        form = KPJForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.data_tk_id = id_tk.pk
            post.no_kpj = form.cleaned_data['no_kpj']
            post.tgl_keps = form.cleaned_data['tgl_keps']
            post.tgl_na = form.cleaned_data['tgl_na']
            # if aktif_na is not None:
            #     post.tgl_na = aktif_na
            #     post.is_aktif = False

            post.save()

            return redirect('home-klaim')
    else:
        form = KPJForm()

    return render(request, 'klaim_registration/input_kpj.html', {'form': form, 'pk': id_tk})


@login_required(login_url='/accounts/login/')
def DetilTK(request, pk):
    datas = DataTK.objects.select_related('hrd').filter(pk=pk)
    data_kpj = KPJ.objects.select_related('data_tk').filter(data_tk__id=pk)
    context = {
        'datas': datas,
        'data_kpj': data_kpj,
    }

    return render(request, 'klaim_registration/detail_tk.html', context)


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
        return JsonResponse({'msg': msg})

    return render(request, 'klaim_registration/tambah_tk.html')


class KlaimListView(ListView):
    model = DataKlaim
    contex_object_name = 'datas'


class KlaimCreateView(CreateView):
    model = DataKlaim
    form_class = KlaimForm
    success_url = reverse_lazy('klaim_changelist')


class KlaimUpdateView(UpdateView):
    model = DataKlaim
    form_class = KlaimForm
    success_url = reverse_lazy('klaim_changelist')


def DaftarKlaim(request):
    # pk = KPJ.objects.select_related('data_tk').get(data_tk__id=pk)
    form = KlaimForm()
    if request.method == 'POST':
        form = KlaimForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save(commit=False)
            # post.no_kpj__data_tk__id = pk
            form.save()
            return redirect('home-klaim')
    return render(request, 'klaim_registration/dataklaim_form.html', {'form': form})


def DaftarKlaimPK(request, pk):
    pk = KPJ.objects.select_related('data_tk').get(data_tk=pk)
    form = KlaimForm()
    if request.method == 'POST':
        form = KlaimForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.no_kpj__data_tk__id = pk
            post.save()
            return redirect('home-klaim')
    return render(request, 'klaim_registration/dataklaim_form.html', {'form': form, 'pk': pk})


def load_sebab(request):
    klaim_id = request.GET.get('klaim_id')
    print(klaim_id)
    sebab = SebabKlaim.objects.filter(tipe_id=klaim_id).order_by('kode')
    return render(request, 'klaim_registration/sebab_dropdown.html', {'sebab': sebab})
