from django.contrib import admin

from .models import DataTK, ApprovalHRD,KPJ, SebabKlaim, TipeKlaim, DataKlaim

admin.site.register(DataTK)
admin.site.register(KPJ)
admin.site.register(SebabKlaim)
admin.site.register(TipeKlaim)
admin.site.register(DataKlaim)
admin.site.register(ApprovalHRD)
# admin.site.register(toQRCode)
