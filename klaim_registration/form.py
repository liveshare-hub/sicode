from django import forms
from django.forms import inlineformset_factory
from django.forms.widgets import Select
# from dal import autocomplete

from .models import KPJ, DataKlaim, DataTK, SebabKlaim, TipeKlaim


class DataTKForm(forms.ModelForm):
    file_lain = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
            }
        ))

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control email',
            'placeholder': 'Masukkan Email Anda'
        })
    )

    class Meta:
        model = DataTK
        exclude = ('hrd',)
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-control besar', 'placeholder': 'INPUT NAMA',
            }),
            'nik': forms.TextInput(attrs={
                'class': 'form-control angka', 'placeholder': 'INPUT NIK',
                'maxlength': "16",
            }),
            'tgl_lahir': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }, format="dd-mm-yyyy"),
            'tempat_lahir': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'INPUT TEMPAT LAHIR',
            }),
            'alamat': forms.TextInput(attrs={
                'class': 'form-control besar', 'placeholder': 'INPUT ALAMAT'
            }),
            'nama_ibu': forms.TextInput(attrs={
                'class': 'form-control besar', 'placeholder': 'NAMA GADIS IBU KANDUNG'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'nama_pasangan': forms.TextInput(attrs={
                'class': 'form-control besar', 'placeholder': 'NAMA SUAMI/ISTRI'
            }),
            'tgl_lahir_pasangan': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }, format="dd-mm-yyyy"),
            'nama_anak_s': forms.TextInput(attrs={
                'class': 'form-control besar', 'placeholder': 'NAMA ANAK PERTAMA'
            }),
            'tgl_lahir_s': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }, format="dd-mm-yyyy"),
            'nama_anak_d': forms.TextInput(attrs={
                'class': 'form-control besar', 'placeholder': 'NAMA ANAK KEDUA'
            }),
            'tgl_lahir_d': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }, format="dd-mm-yyyy"),
            'no_hp': forms.TextInput(attrs={
                'class': 'form-control angka', 'placeholder': 'NO HANDPHONE/WA',
                'maxlength': "13"
            }),
            'nama_rekening': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'NAMA PEMILIK REKENING'
            }),
            'no_rekening': forms.TextInput(attrs={
                'class': 'form-control angka', 'placeholder': 'NO REKENING'
            }),
            'propic': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'file_kk': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'file_ktp': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'file_paklaring': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            # 'file_lain':forms.FileInput(attrs={
            #     'class':'form-control'
            # }),
        }


class KPJForm(forms.ModelForm):
    class Meta:
        model = KPJ
        exclude = ('data_tk',)
        widgets = {
            'no_kpj': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Input No KPJ',
                'maxlength': '11'
            }),
            'tgl_keps': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'tgl_na': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            })
        }


KpjInlineFormset = inlineformset_factory(DataTK, KPJ, fields=(
    'no_kpj', 'tgl_keps', 'tgl_na',), extra=1, can_delete=False)


class KlaimFormPK(forms.ModelForm):
    tipe_klaim = forms.ModelChoiceField(queryset=TipeKlaim.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = DataKlaim
        exclude = ('no_kpj',)

        widgets = {
            'sebab_klaim': forms.Select(attrs={
                'class': 'form-control',
            }),
            'surat_meinggal': forms.FileInput(attrs={'class': 'form-control'}),
            'ktp_ahli_waris': forms.FileInput(attrs={'class': 'form-control'}),
            'kk_baru': forms.FileInput(attrs={'class': 'form-control'}),
            'no_rek_waris': forms.FileInput(attrs={'class': 'form-control'}),
            'form_I': forms.FileInput(attrs={'class': 'form-control'}),
            'kronologis': forms.FileInput(attrs={'class': 'form-control'}),
            'ktp_saksi': forms.FileInput(attrs={'class': 'form-control'}),
            'absen_1': forms.FileInput(attrs={'class': 'form-control'}),
            'surat_pernyataan': forms.FileInput(attrs={'class': 'form-control'}),
            'form_II': forms.FileInput(attrs={'class': 'form-control'}),
            'absensi_2': forms.FileInput(attrs={'class': 'form-control'}),
            'no_rek_perusahaan': forms.FileInput(attrs={'class': 'form-control'}),
            'no_rek_tk': forms.FileInput(attrs={'class': 'form-control'}),
            'slip_gaji': forms.FileInput(attrs={'class': 'form-control'}),
            'parklaring': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sebab_klaim'].queryset = SebabKlaim.objects.none()

        if 'tipe_klaim' in self.data:
            try:
                tipe_id = int(self.data.get('tipe_klaim'))
                self.fields['sebab_klaim'].queryset = SebabKlaim.objects.filter(
                    tipe_id=tipe_id).order_by('kode')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['sebab_klaim'].queryset = self.instance.sebab_klaim.tipe_klaim_set.order_by(
                'kode')
