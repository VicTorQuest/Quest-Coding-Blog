from django import forms
from django.contrib.auth.models import User
from store.models import BillingAddress, Customer
from django_countries.widgets import CountrySelectWidget


class EditAccount(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super(EditAccount, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['autofocus'] = 'true'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['autofocus'] = 'false'
        self.fields['email'].widget.attrs['class'] = 'form-control'

class EditCustomer(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name',
            'email',
            'phone_number'
        ]
    
    def __init__(self, *args, **kwargs):
        super(EditCustomer, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'


class EditBillingAddress(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = [
            'address',
            'country',
            'state',
            'city',
            'zipcode'
        ]
        widgets = {'country': CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        super(EditBillingAddress, self).__init__(*args, **kwargs)

        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['state'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['zipcode'].widget.attrs['class'] = 'form-control'
# class UserupdateForm(forms.ModelForm):
#     first_name = forms.CharField(
#         label='First Name',
#         max_length=50,
#         widget=forms.TextInput(
#             attrs={
#                 'autofocus': 'true',
#                 'class': 'form-control mb-3'
#             }
#         )
#     )

#     last_name = forms.CharField(
#         label='Last Name',
#         max_length=50,
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control mb-3'
#             }
#         )
#     )
#     class Meta:
#         model = User
#         fields = [
#             'first_name',
#             'last_name',
#             'username',
#             'email'
#         ]
#     def __init__(self, *args, **kwargs):
#         super(UserupdateForm, self).__init__(*args, **kwargs)

#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['username'].widget.attrs['autofocus'] = 'false'
#         self.fields['email'].widget.attrs['class'] = 'form-control mb-3'
    