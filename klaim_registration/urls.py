from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views
# from .views import nppAutoComplete

urlpatterns = [
    path('', views.index, name='home-klaim'),
    path('tambah/tk', views.TambahTK, name='tambah-tk'),
    path('tambah/tk/ajax', views.TambahTK_ajax, name='tambah-tk-ajax'),
    path('tambah/kpj/<int:pk>', views.tambah_kpj, name='tambah-kpj'),
    path('detil/tk/<int:pk>', views.DetilTK, name='detil-tk'),
    path('ajax/tk/<int:pk>', views.detilKlaimAjax, name='detil-tk-ajax'),
    path('api/kpj', views.ListKPJ.as_view(), name='api-kpj'),
    path('klaim/tambah/ajax', views.ajaxKlaim, name='tambah-klaim-ajax'),
    path('klaim/tambah', views.DaftarKlaim, name='tambah-klaim'),
    path('klaim/tambah/<int:pk>', views.DaftarKlaimPK, name='tambah-klaim-pk'),
    path('klaim/edit/<int:pk>', views.KlaimUpdateView.as_view(), name='klaim-edit'),
    path('ajax/load-klaims', views.load_sebab, name='ajax_load_sebab'),
    path('hrd/approval', views.listApproval, name='list-approval'),
    path('hrd/approval/ajax', views.ajaxApproval, name='ajax-approval'),
    # path('qr-code/<str:uid>/', views.detail_tk, name='detail-tk'),
    path('email/<int:pk>/sent', views.sent_mail, name='sent-mail'),
    # path('klaim/zip/<int:id>/', views.zipAll, name='zip-file'),
    # re_path(
    #     r'^npp-autocomplete/$',
    #     nppAutoComplete.as_view(),
    #     name='npp-autocomplete',
    # ),

]
