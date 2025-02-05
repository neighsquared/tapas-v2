from django.apps import forms
from .models import Supplier, WaterBottle, Account

class SupplierForm(forms.ModelForm):
    item_name = forms.ModelChoiceField(
        label="Supplier", queryset=Supplier.objects.name(), required=True
    )