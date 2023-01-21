from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Post



def post_changed(sender, **kwargs):
    if kwargs['instance'].category.count() > 3:
        raise ValidationError(_("You can't assign more than three regions"))


m2m_changed.connect(post_changed, sender=Post.category.through)
