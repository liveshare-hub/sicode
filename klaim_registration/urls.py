from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views
# from .views import nppAutoComplete

urlpatterns = [
    path('', views.index, name='home-klaim'),
    path('tambah/tk', views.TambahTK, name='tambah-tk'),

    # path('daftar/', views.tambahKlaim1, name='add'),
    # path('hrd/klaim/', views.daftarKlaimHRD,
    #      name='hrd-klaim'),
    # path('hrd/klaim/', views.get_detail_tk, name='get-detail'),

    # path('hrd/klaim/<int:klaim_id>/',
    #      views.get_klaimhrd_json, name='klaim-detail'),
    # path('qr-code/<str:uid>/', views.detail_tk, name='detail-tk'),
    # path('email/<int:id>/sent/', views.sent_mail, name='sent-mail'),
    # path('klaim/zip/<int:id>/', views.zipAll, name='zip-file'),
    # re_path(
    #     r'^npp-autocomplete/$',
    #     nppAutoComplete.as_view(),
    #     name='npp-autocomplete',
    # ),

]
