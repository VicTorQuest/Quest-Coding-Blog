from better_profanity import profanity
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Comment, Post
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = "__all__"

        def clean_category(self):
            category =  self.cleaned_data['category']
            if category.count() > 3:
                raise ValidationError(_("You can't assign more than 3 categories"))
            return category

        def __init__(self, *args, **kwargs):
            super(PostForm, self).__init__(*args, **kwargs)
            if self.instance.pk:
                self.fields['category'].queryset = Post.objects.filter(category=self.instance.category)
            


custom_bad_words = ['nigga', 'nigger', 'fag', 'faggot']
profanity.add_censor_words(custom_bad_words)

class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
    
    def clean_name(self):
        value = self.cleaned_data['name']
        bad_words = profanity.contains_profanity(value)
        if bad_words:
            raise ValidationError(_("the use of profanity is prohibited in this platform"))
        updated_value = profanity.censor(value)
        return updated_value


    def clean_body(self):
        value = self.cleaned_data['body']
        bad_words = profanity.contains_profanity(value)
        if bad_words:
            raise ValidationError(_("the use of profanity is prohibited in this platform"))
        updated_value = profanity.censor(value)
        return updated_value


    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control mb-4'
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['email'].widget.attrs['class'] = 'form-control mb-4'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['body'].widget.attrs['class'] = 'form-control mb-4'
        self.fields['body'].widget.attrs['placeholder'] = 'Comment'


class CreatePostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'intro',
            'post_img',
            'content',
        ]