from django import forms
from django.utils.translation import gettext_lazy as _  
from .models import Foods, Pictures
from datetime import datetime

class FoodForm(forms.ModelForm):
    class Meta:
        model = Foods
        fields = ["name", "category", "expirydate", "quantity"]
        labels = {
            'name': _('食品名'),
            'category': _('カテゴリ'),
            'expirydate': _('保存期限'),
            'quantity': _('残量'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('入力してください')}),
            'expirydate': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class FoodUpdateForm(forms.ModelForm):
    class Meta:
        model = Foods
        fields = ["name", "category", "expirydate", "quantity"]
        labels = {
            'name': _('食品名'),
            'category': _('カテゴリ'),
            'expirydate': _('保存期限'),
            'quantity': _('残量'),
        }
        widgets = {
            'expirydate': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class PictureUploadForm(forms.ModelForm):
    class Meta:
        model = Pictures
        fields = ['picture']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True, food=None):
        instance = super(PictureUploadForm, self).save(commit=False)
        if food is not None:
            instance.food = food
        if commit:
            instance.save()
        return instance