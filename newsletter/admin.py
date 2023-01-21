from django.contrib import admin
from .models import Subscriber, MailMessage, UnsubscribedEmail

# Register your models here.
class SubscribersFormat(admin.ModelAdmin):
    search_fields = ['email']
    list_display = ['email', 'first_name', 'last_name', 'subscribed_on']
    
class UnsubscribedEmailFormat(admin.ModelAdmin):
    search_fields = ['email']
    list_display = ['__str__', 'date']
admin.site.register(Subscriber, SubscribersFormat)
admin.site.register(MailMessage)
admin.site.register(UnsubscribedEmail, UnsubscribedEmailFormat)
