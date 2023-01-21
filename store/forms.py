from django import forms
from .models import Refund, OrderItem


class RefundForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        order_queryset = kwargs.pop('order_queryset')
        super(RefundForm, self).__init__(*args, **kwargs)
        self.fields['items'].queryset = OrderItem.objects.filter(order=order_queryset)



    class Meta:
        model = Refund
        fields = [
            'items'
        ]

    items = forms.ModelMultipleChoiceField(label="Bought items:",queryset=None, widget=forms.CheckboxSelectMultiple())
