from django.contrib import admin

from .models import DataTK, ApprovalHRD, toQRCode, KPJ

admin.site.register(DataTK)
admin.site.register(KPJ)
# admin.site.register(DaftarHRD)
admin.site.register(ApprovalHRD)
admin.site.register(toQRCode)
