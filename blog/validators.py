from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from better_profanity import profanity
from newsletter.models import Subscriber


def validate_name(value):
    if len(value) < 3:
        raise ValidationError(_(f"The name '{value}' is too short. Enter a real name"))
    return value

def validate_email(value):
    if (value.startswith('abc')) or (value.startswith('123')):
        raise ValidationError(_("Dummy data like 'abc' or '123' is not allowd"))
    return value

def validate_subscriber_email(value):
    if Subscriber.objects.filter(email=value).exists():
        raise ValidationError(_("{} is already subscribed to Quest Coding newsletter".format(value)))
    return value


def restrict_vulger_words(value):
    bad_words = profanity.contains_profanity(value)
    print(bad_words)
    if bad_words:
        raise ValidationError(_("the use of profanity is prohibited in this platform"))
    return value