from dataclasses import field
from django import forms
from .models import Subscriber, MailMessage, UnsubscribedEmail
from blog.validators import validate_email, validate_subscriber_email, validate_name
from  django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox




class Subscribetoletter(forms.ModelForm):
    email = forms.CharField(label='Email Address', validators=[validate_subscriber_email, validate_email],widget=forms.EmailInput(
        attrs={"class": "form-control"}
    ))

    first_name = forms.CharField(label='First Name', validators=[validate_name],widget=forms.TextInput(
        attrs={"class": "form-control"}
    ))

    last_name = forms.CharField(label='First Name', validators=[validate_name],widget=forms.TextInput(
        attrs={"class": "form-control"}
    ))

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    class Meta:
        model = Subscriber
        fields = [
            'email',
            'first_name',
            'last_name'
        ]


class EditPreference(forms.ModelForm):
    email = forms.CharField(label='Email Address', validators=[validate_email],widget=forms.EmailInput(
        attrs={"class": "form-control"}
    ))

    first_name = forms.CharField(label='First Name', validators=[validate_name],widget=forms.TextInput(
        attrs={"class": "form-control"}
    ))

    last_name = forms.CharField(label='Last Name', validators=[validate_name],widget=forms.TextInput(
        attrs={"class": "form-control"}
    ))
    
    class Meta:
        model = Subscriber
        fields = [
            'email',
            'first_name',
            'last_name'
        ]


class SendNewsLetter(forms.ModelForm):
    title = forms.CharField(label='Title', widget=forms.TextInput(
        attrs={"class": "form-control"}
    ))

    message = forms.CharField(label='Message', widget=forms.Textarea(
        attrs={"class": "form-control "}
    ))
    class Meta:
        model = MailMessage
        fields = "__all__"

class UnsubscribedEmailReason(forms.ModelForm):
    reasons = [("I no longer want to receive this email", "I no longer want to receive this email"), ("I never signed up for this email list", "I never signed up for this email list"), ("The emails are inappropriate","The emails are inappropriate"), ("The emails are spam and should be reported", "The emails are spam and should be reported")]
    reason = forms.ChoiceField(choices=reasons, label='',widget=forms.RadioSelect())

    class Meta:
        model = UnsubscribedEmail
        fields = [
            'reason'
        ]