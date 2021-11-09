from django.contrib import admin

from .models import DataTK, ApprovalHRD, toQRCode, KPJ, SebabKlaim, TipeKlaim

admin.site.register(DataTK)
admin.site.register(KPJ)
admin.site.register(SebabKlaim)
admin.site.register(TipeKlaim)
# admin.site.register(DaftarHRD)
admin.site.register(ApprovalHRD)
admin.site.register(toQRCode)
