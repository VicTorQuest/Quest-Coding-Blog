from django.db import models
from .utils import generate_slug
from .thread import SendNewsLetter



# Create your models here.
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=25, null=True)
    slug = models.SlugField(null=True, blank=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug is None:
            self.slug = generate_slug(self)
        super(Subscriber, self).save(*args, **kwargs)


class MailMessage(models.Model):
    SEND = 'yes'
    DONT_SEND = 'no'

    CHOICES_STATUS = (
        (SEND, 'yes'),
        (DONT_SEND, 'no')
    )

    title = models.CharField(max_length=150)
    content_image_link = models.URLField(null=True)
    message = models.TextField()
    content_link = models.URLField(null=True)
    link_subject = models.CharField(default="Read article", max_length=20)
    send_news_letter = models.CharField(max_length=10, null=True, choices=CHOICES_STATUS, default=SEND)
    Created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}....".format(self.title, self.message[:25])

    def save(self, *args, **kwargs,):
        super().save(*args, **kwargs)
        
        if self.send_news_letter == MailMessage.SEND:
            email_list = []
            subscribers = Subscriber.objects.all()
            for member in subscribers:
                email_list.append(member)
            
            SendNewsLetter(obj=self, email_list=email_list).start()
            self.send_news_letter = MailMessage.DONT_SEND
        super(MailMessage, self).save(*args, **kwargs)
                
                
        

class UnsubscribedEmail(models.Model):
    email = models.EmailField()
    reason = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{}: {}....".format(self.email, self.reason[:35])