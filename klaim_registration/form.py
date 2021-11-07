from django import forms
from django.forms import inlineformset_factory
# from dal import autocomplete

from .models import KPJ, DataKlaim, DataTK


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
