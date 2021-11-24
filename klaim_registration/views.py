from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.hashers import make_password
# from django.contrib import messages
# from django.contrib.auth.models import User, Group
from django.utils.html import strip_tags
from django.db.models import Subquery, OuterRef, Q
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
# from dal import autocomplete
# import random
# import string

from django.conf import settings

from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework.generics import ListCreateAPIView

from klaim_registration.serializer import KPJSerializer

from .form import DataTKForm, KPJForm, KlaimFormPK
from .models import KPJ, DataKlaim, ApprovalHRD, DataTK, SebabKlaim
# from authentication.models import Perusahaan, Profile
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


class KlaimUpdateView(UpdateView):
    model = DataKlaim
    form_class = KlaimFormPK
    success_url = reverse_lazy('klaim_changelist')


@login_required(login_url='/accounts/login/')
def DaftarKlaim(request):
    # pk = KPJ.objects.select_related('data_tk').get(data_tk__id=pk)
    form = KlaimFormPK()
    # if request.method == 'POST':
    #     form = KlaimFormPK(request.POST, request.FILES)
    #     if form.is_valid():
    #         # form.save(commit=False)
    #         # post.no_kpj__data_tk__id = pk
    #         form.save()
    #         return redirect('home-klaim')
    return render(request, 'klaim_registration/klaim_form.html', {'form': form})


@csrf_exempt
def ajaxKlaim(request):

    parklaring = request.FILES.get('parklaring')
    # surat_meninggal = request.FILES.get('surat_meninggal')
    # ktp_ahli_waris = request.FILES.get('ktp_ahli_waris')
    # kk_baru = request.FILES.get('kk_baru')
    # no_rek_waris = request.FILES.get('no_rek_waris')
    # form_I = request.FILES.get('form_I')
    # kronologis = request.FILES.get('kronologis')
    # ktp_saksi = request.FILES.get('ktp_saksi')
    # absen_1 = request.FILES.get('absen_1')
    # surat_pernyataan = request.FILES.get('surat_pernyataan')
    # form_II = request.FILES.get('form_II')
    # absensi_2 = request.FILES.get('absensi_2')
    # no_rek_perusahaan = request.FILES.get('no_rek_perusahaan')
    no_rek_tk = request.FILES.get('no_rek_tk')
    # slip_gaji = request.FILES.get('slip_gaji')
    # no_rek_tk = request.FILES.get('no_rek_tk')
    tipe_klaim = request.POST.get('tipe_klaim')
    sebab_klaim = request.POST.get('tipe_klaim')
    no_kpj = request.POST.get('kpj')
    kpj = KPJ.objects.get(no_kpj=no_kpj)
    fss = FileSystemStorage()
    filename1 = fss.save(parklaring.name, parklaring)
    filename2 = fss.save(no_rek_tk.name, no_rek_tk)
    # file3 = fss.save(surat_meninggal.name, surat_meninggal)
    # file4 = fss.save(ktp_ahli_waris.name, ktp_ahli_waris)
    # file5 = fss.save(kk_baru.name, kk_baru)
    # file6 = fss.save(no_rek_waris.name, no_rek_waris)
    # file7 = fss.save(form_I.name, form_I)
    # file8 = fss.save(kronologis.name, kronologis)
    # file9 = fss.save(ktp_saksi.name, ktp_saksi)
    # file10 = fss.save(absen_1.name, absen_1)
    # file11 = fss.save(surat_pernyataan.name, surat_pernyataan)
    # file12 = fss.save(form_II.name, form_II)
    # file13 = fss.save(absensi_2.name, absensi_2)
    # file14 = fss.save(no_rek_perusahaan.name, no_rek_perusahaan)
    # file15 = fss.save(slip_gaji.name, slip_gaji)
    url1 = fss.url(filename1)
    url2 = fss.url(filename2)
    # url3 = fss.url(file3)
    # url4 = fss.url(file4)
    # url5 = fss.url(file5)
    # url6 = fss.url(file6)
    # url7 = fss.url(file7)
    # url8 = fss.url(file8)
    # url9 = fss.url(file9)
    # url10 = fss.url(file10)
    # url11 = fss.url(file11)
    # url12 = fss.url(file12)
    # url13 = fss.url(file13)
    # url14 = fss.url(file14)
    # url15 = fss.url(file15)
    try:
        DataKlaim.objects.create(
            sebab_klaim_id=sebab_klaim,
            tipe_klaim_id=tipe_klaim,
            parklaring=url1,
            no_rek_tk=url2,
            no_kpj_id=kpj.id

        )

        return JsonResponse({'success': 'Berhasil!'})
    except:
        return JsonResponse({'error': 'Errors!'})


def detilKlaimAjax(request, pk):
    tk = list(ApprovalHRD.objects.select_related('klaim', 'hrd').filter(
        pk=pk).values('klaim__parklaring', 'klaim__no_rek_tk'))
    return JsonResponse({'data': tk})


@login_required(login_url='/accounts/login/')
def DaftarKlaimPK(request, pk):
    pk = KPJ.objects.select_related('data_tk').get(pk=pk)
    form = KlaimFormPK()
    if request.method == 'POST':
        form = KlaimFormPK(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.no_kpj__data_tk__id = pk
            post.save()
            return redirect('home-klaim')
    return render(request, 'klaim_registration/dataklaim_form.html', {'form': form, 'pk': pk})


@login_required(login_url='/accounts/login/')
def load_sebab(request):
    klaim_id = request.GET.get('klaim_id')
    # print(klaim_id)
    sebab = SebabKlaim.objects.filter(tipe_id=klaim_id).order_by('kode')
    return render(request, 'klaim_registration/sebab_dropdown.html', {'sebab': sebab})


@login_required(login_url='/accounts/login/')
def listApproval(request):
    hrd = request.user.profile
    datas = ApprovalHRD.objects.select_related(
        'klaim', 'hrd').filter(hrd=hrd)
    context = {
        'datas': datas
    }
    return render(request, 'klaim_registration/hrd1.html', context)


def ajaxApproval(request):
    if request.is_ajax:
        ApprovalHRD.objects.filter(pk=request.POST.get('id')).update(
            status=request.POST.get('status'), keterangan=request.POST.get('keterangan')
        )
        return JsonResponse({'success': 'Data Berhasil Di Simpan'})

# def validasi_berkas(request):

def sent_mail(request, pk):
    tk_id = ApprovalHRD.objects.select_related('klaim','hrd').get(pk=pk)
    qrcode = tk_id.img_svg
    to = tk_id.klaim.no_kpj.data_tk.email
    im = Image.open(qrcode.file)
    print(qrcode.file)
    bg = Image.new("RGB", (450,450), "white")
    bg.paste(im, (0,0), im)
    bg.save(qrcode.name + ".jpg", quality=95)
    context = {
        'nama':tk_id.klaim.no_kpj.data_tk.nama,
        'propic':tk_id.klaim.no_kpj.data_tk.propic,
        'qrcode':qrcode
    }
    html_content = render_to_string('klaim_registration/email.html', context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        #subject
        f"DETAIL DATA TK A.N {tk_id.klaim.no_kpj.data_tk.nama}",
        #content
        text_content,
        #from email
        settings.EMAIL_HOST_USER,
        #to email
        [to]
    )
    email.attach_alternative(html_content, "text/html")
    filename = '/home/sicm6455/python/' + qrcode.url
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= "+filename)
    email.attach(part)
    email.send()

    return JsonResponse({'success':'Email Berhasil Terkirim'})


class ListKPJ(ListCreateAPIView):
    serializer_class = KPJSerializer
    permission_classes = [permissions.AllowAny, ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['no_kpj', ]
    search_fields = ['no_kpj', ]

    def get_queryset(self):
        qs = KPJ.objects.select_related('data_tk').all()
        if qs.exists():
            return qs
        else:
            return qs.none()
