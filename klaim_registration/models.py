from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from PIL import Image, ImageDraw
import uuid
import hashlib
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
import qrcode
from io import BytesIO
from django.core.files import File
from datetime import datetime

from authentication.models import Profile
# from .uuid_gen import autoGen

NIK_VALIDATOR = RegexValidator("^\d{16}$",
                               "Format NIK Tidak Sesuai")

HP_VALIDATOR = RegexValidator(
    "^(08+[1-9])([0-9]{7,9})$", "Format NO HP TIDAK SESUA!!!")

NO_REK_VALIDATOR = RegexValidator("^\d{6,}$", "No Rekening Harus Berupa Angka")

EKSTENSI_VALIDATOR = RegexValidator(
    ".*\.(jpg|JPG|JPEG|pdf|PDF)", "Only Support PDF dan JPG")

SEGMEN = (
    ('PU', 'PENERIMA UPAH'),
    ('BPU', 'BUKAN PENERIMA UPAH'),
    ('JAKON', 'JASA KONSTRUKSI'),
)

STATUS = (
    ('BELUM MENIKAH', 'BELUM MENIKAH'),
    ('MENIKAH', 'MENIKAH')
)

STATUS_APPROVAL = (
    ('DALAM PEMERIKSAAN', 'DALAM PEMERIKSAAN'),
    ('DISETUJUI', 'DISETUJUI'),
    ('DITOLAK', 'DITOLAK')
)


class TipeKlaim(models.Model):
    kode = models.CharField(max_length=5)
    tipe_klaim = models.CharField(max_length=3)

    def __str__(self):
        return '{} - {}'.format(self.kode, self.tipe_klaim)


class SebabKlaim(models.Model):
    tipe = models.ForeignKey(TipeKlaim, on_delete=models.CASCADE)
    kode = models.CharField(max_length=5)
    sebab_klaim = models.CharField(max_length=200)
    keyword = models.CharField(max_length=3)

    def __str__(self):
        return '{} - {}'.format(self.kode, self.sebab_klaim)


class DataTK(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    hrd = models.ForeignKey(Profile, on_delete=models.CASCADE)
    nama = models.CharField(max_length=200)
    nik = models.CharField(max_length=16, validators=[NIK_VALIDATOR])
    # kpj = models.CharField(max_length=11)
    # npp = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)
    tgl_lahir = models.DateField()
    tempat_lahir = models.CharField(max_length=200)
    alamat = models.CharField(max_length=250)
    nama_ibu = models.CharField(max_length=100)
    status = models.CharField(
        choices=STATUS, max_length=13, default='BELUM MENIKAH')
    nama_pasangan = models.CharField(max_length=100, null=True, blank=True)
    tgl_lahir_pasangan = models.DateField(blank=True, null=True)
    nama_anak_s = models.CharField(max_length=100, blank=True, null=True)
    tgl_lahir_s = models.DateField(null=True, blank=True)
    nama_anak_d = models.CharField(max_length=100, blank=True, null=True)
    tgl_lahir_d = models.DateField(null=True, blank=True)
    no_hp = models.CharField(max_length=15, validators=[HP_VALIDATOR])
    email = models.EmailField(max_length=200, null=True, blank=True)
    nama_rekening = models.CharField(max_length=100)
    no_rekening = models.CharField(
        max_length=16, validators=[NO_REK_VALIDATOR])
    propic = models.ImageField(upload_to='profile/tk/', blank=True, null=True)
    file_kk = models.FileField(
        upload_to='tk/kk/', validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    file_ktp = models.FileField(
        upload_to='tk/ktp/', validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    # file_paklaring = models.FileField(
    #     upload_to='tk/paklaring/', validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    # file_lain = models.FileField(
    #     upload_to='lain/', null=True, blank=True, validators=[EKSTENSI_VALIDATOR])
    qr_code_tk = models.ImageField(upload_to='qrcode/tk/')
    url_id = models.CharField(max_length=64)
    edited_on = models.DateTimeField(auto_created=True)
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "DATA TK"
        verbose_name_plural = "LIST DATA TK"

    def __str__(self):
        return '{} - {}'.format(self.nik, self.nama)

    def save(self, *args, **kwargs):
        strings = str(self.nama+self.nik).encode('utf-8')
        self.url_id = hashlib.sha256(strings).hexdigest()
        url = "https://sicode.id/detail/tk/{}".format(self.url_id)
        qr = qrcode.QRCode(
            version=20,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=50,
            border=2,
        )
        # qr.add_data('https://sicode.id/qr-code/{}'.format(self.url_uuid))
        # qr.add_data('http://127.0.0.1/qr-code/{}/'.format(self.url_uuid))
        # qr.make(fit=False)
        # qrcode_image = qrcode.make(
        # 'http://127.0.0.1:8000/qr-code/{}/'.format(self.url_uuid))
        # qrcode_image = qr.make_image(fill_color="black", back_color="white")
        qrcode_image = qrcode.make(url)

        canvas = Image.new('RGB', (450, 450), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        # uid = uuid.uuid4()
        fname = '{}.jpg'.format(self.nama)
        buffer = BytesIO()
        canvas.save(buffer, 'jpeg')
        # qrcode_image.save(buffer, 'PNG')
        self.qr_code_tk.save(fname, File(buffer), save=False)
        canvas.close()

        super().save(*args, **kwargs)


class KPJ(models.Model):
    data_tk = models.ForeignKey(
        DataTK, on_delete=models.CASCADE, related_name="list_kpj")
    no_kpj = models.CharField(max_length=11, null=True, blank=True)
    tgl_keps = models.DateField(null=True, blank=True)
    tgl_na = models.DateField(blank=True, null=True)
    is_aktif = models.BooleanField(default=False)

    def __str__(self):
        if self.no_kpj:
            return '{} - {}'.format(self.no_kpj, self.data_tk.nama)
        else:
            return self.data_tk.nama

    def save(self, *args, **kwargs):
        if self.tgl_na is None:

            self.is_aktif = True
        else:
            self.is_aktif = False
        super(KPJ, self).save(*args, **kwargs)


# @receiver(post_save, sender=DataTK)
# def post_save_KPJ(sender, instance, created, **kwargs):
#     if created:
#         KPJ.objects.create(data_tk=instance)


class DataKlaim(models.Model):
    no_kpj = models.ForeignKey(KPJ, on_delete=models.CASCADE)
    tipe_klaim = models.ForeignKey(TipeKlaim, on_delete=models.CASCADE)
    sebab_klaim = models.ForeignKey(SebabKlaim, on_delete=models.CASCADE)
    parklaring = models.FileField(
        upload_to='jhtjp/parklaring/', validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    surat_meinggal = models.FileField(
        upload_to='jkm/surat_meinggal/', validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    ktp_ahli_waris = models.FileField(
        upload_to='jkm/ktp_ahliwaris/', validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    kk_baru = models.FileField(
        upload_to='jkm/kk_baru/', validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    no_rek_waris = models.FileField(
        upload_to='jkm/no_rek_ahli_waris/', validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    form_I = models.FileField(upload_to='jkk/tahap_I/form/',
                              validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    kronologis = models.FileField(
        upload_to='jkk/tahap_I/kronologis/', validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    ktp_saksi = models.FileField(upload_to='jkk/tahap_I/ktp_saksi/',
                                 validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    absen_1 = models.FileField(upload_to='jkk/tahap_I/absen_1/',
                               validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    surat_pernyataan = models.FileField(
        upload_to='jkk/tahap_I/surat_pernyataan/', validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    form_II = models.FileField(upload_to='jkk/tahap_II/form/',
                               validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    absensi_2 = models.FileField(upload_to='jkk/tahap_II/absensi_2/',
                                 validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    no_rek_perusahaan = models.FileField(
        upload_to='jkk/tahap_II/no_rek_pers/', validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    no_rek_tk = models.FileField(upload_to='jkk/tahap_II/no_rek_tk',
                                 validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    slip_gaji = models.FileField(
        upload_to='jkk/tahap_II/slip/', validators=[EKSTENSI_VALIDATOR], blank=True, null=True)
    flag_klaim = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.no_kpj.no_kpj, self.no_kpj.data_tk.nama)

    def save(self, *args, **kwargs):
        self.flag_klaim = True
        # if (self.flag_klaim is True and self.no_kpj.tgl_na is None):
        #     self.no_kpj.is_aktif = False
        #     self.no_kpj.tgl_na = datetime.today()

        super().save(*args, **kwargs)


@receiver(post_save, sender=DataKlaim)
def Approval(sender, instance, created, **kwargs):
    print(instance.no_kpj.data_tk.hrd.user.pk)
    if created:
        # hrd = DataKlaim.objects.select_related('no_kpj').get(no_kpj_id=kwargs)
        ApprovalHRD.objects.create(
            klaim=instance, hrd_id=instance.no_kpj.data_tk.hrd.user.pk)


# class DaftarHRD(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     nama = models.CharField(max_length=100)
#     npp = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name_plural = "LIST HRD"

#     def __str__(self):
#         return self.nama


class ApprovalHRD(models.Model):
    # status = models.CharField(choices=STATUS_APPROVAL,
    #                           default='DALAM PEMERIKSAAN', max_length=20)
    klaim = models.ForeignKey(DataKlaim, on_delete=models.CASCADE)
    hrd = models.ForeignKey(Profile, on_delete=models.CASCADE)
    url_uuid = models.UUIDField(default=uuid.uuid4())
    img_svg = models. ImageField(upload_to='qrcode/klaim/tk/')
    # keterangan = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.klaim.no_kpj.no_kpj

    def save(self, *args, **kwargs):
        url = "https://sicode.id/detail/klaim/{}".format(self.url_uuid)
        qr = qrcode.QRCode(
            version=20,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=50,
            border=2,
        )
        # qr.add_data('https://sicode.id/qr-code/{}'.format(self.url_uuid))
        # qr.add_data('http://127.0.0.1/qr-code/{}/'.format(self.url_uuid))
        # qr.make(fit=False)
        # qrcode_image = qrcode.make(
        # 'http://127.0.0.1:8000/qr-code/{}/'.format(self.url_uuid))
        # qrcode_image = qr.make_image(fill_color="black", back_color="white")
        qrcode_image = qrcode.make(url)

        canvas = Image.new('RGB', (450, 450), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        # uid = uuid.uuid4()
        fname = '{}.jpg'.format(self.klaim.no_kpj.data_tk.nama)
        buffer = BytesIO()
        canvas.save(buffer, 'jpeg')
        # qrcode_image.save(buffer, 'PNG')
        self.img_svg.save(fname, File(buffer), save=False)
        canvas.close()
        # qrcode_image.close()
        super().save(*args, **kwargs)

# class toQRCode(models.Model):
#     tk_klaim = models.ForeignKey(ApprovalHRD, on_delete=models.CASCADE)
#     url_uuid = models.UUIDField(default=uuid.uuid4(), editable=False)
#     img_svg = models.ImageField(upload_to='qrcode/')

#     def __str__(self):
#         return self.tk_klaim.klaim.nama

#     def save(self, *args, **kwargs):
#         qr = qrcode.QRCode(
#             version=20,
#             error_correction=qrcode.constants.ERROR_CORRECT_M,
#             box_size=30,
#             border=4,
#         )
#         qr.add_data('https://sicode.id/qr-code/{}/'.format(self.url_uuid))
#         # qr.add_data('http://127.0.0.1/qr-code/{}/'.format(self.url_uuid))
#         qr.make(fit=False)
#         # qrcode_image = qrcode.make(
#         # 'http://127.0.0.1:8000/qr-code/{}/'.format(self.url_uuid))
#         qrcode_image = qr.make_image(fill_color="black", back_color="white")

#         canvas = Image.new('RGB', (300, 300), 'white')
#         draw = ImageDraw.Draw(canvas)
#         canvas.paste(qrcode_image)
#         # uid = uuid.uuid4()
#         fname = '{}.PNG'.format(self.tk_klaim.klaim.no_kpj.data_tk.nama)
#         buffer = BytesIO()
#         canvas.save(buffer, 'PNG')
#         # qrcode_image.save(buffer, 'PNG')
#         self.img_svg.save(fname, File(buffer), save=False)
#         canvas.close()
#         # qrcode_image.close()
        # super().save(*args, **kwargs)
