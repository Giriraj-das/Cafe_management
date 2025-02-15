from django import forms
from django.forms import formset_factory
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'status']


class DishForm(forms.Form):
    name = forms.CharField(label="Блюдо", max_length=255)
    price = forms.DecimalField(label="Стоимость", max_digits=10, decimal_places=2, min_value=0)
    quantity = forms.IntegerField(label="Количество", min_value=1, initial=1)


DishFormSet = formset_factory(DishForm, extra=1, can_delete=True)
