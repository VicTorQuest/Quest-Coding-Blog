import threading
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse
from django.template.loader import get_template


domain_name = getattr(settings, 'DOMAIN_NAME', 'questcoding.blog')
from_this_email = getattr(settings, 'APPLICATION_EMAIL', "questcoding2001gmail.com")

class EmailThreading(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=True)

class SendNewsLetter(threading.Thread):
    def __init__(self, obj, email_list):
        self.obj = obj
        self.email_list = email_list
        threading.Thread.__init__(self)

    def run(self):
        subject = self.obj.title
        message = self.obj.message
        html_template_path = "newsletter/newsletter_email.html"

        email_msg = EmailMultiAlternatives()
        connection = email_msg.get_connection()              
        connection.open()    
        for subscriber in self.email_list:
            context_data = {'edit_preference': domain_name + reverse('edit_preference', kwargs={'slug': subscriber.slug}), 'unsubscribe': domain_name + reverse('unsubscribe', kwargs={'slug': subscriber.slug}), "privacy_link": domain_name + reverse('privacy'), "message":message, "first_name": subscriber.first_name, "last_name": subscriber.last_name, "img_link": self.obj.content_image_link, "content_link": self.obj.content_link, "link_subject": self.obj.link_subject, 'email': subscriber.email}
            email_html_template = get_template(html_template_path).render(context_data)
            email_msg.subject = subject
            email_msg.from_email = from_this_email
            email_msg.to = [subscriber.email]
            email_msg.body = email_html_template
            email_msg.reply_to = [from_this_email]
            email_msg.content_subtype = 'html'
            email_msg.attach_alternative = (email_html_template, "text/html")
            email_msg.connection = connection
            email_msg.send(fail_silently=True)
        connection.close()