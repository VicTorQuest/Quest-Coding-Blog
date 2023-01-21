import threading
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from_this_email = getattr(settings, 'APPLICATION_EMAIL', "questcoding2001gmail.com")

class SendThreadEmail(threading.Thread):
    def __init__(self, obj, post, link):
        self.obj = obj
        self.post = post
        self.link = link

        threading.Thread.__init__(self)

    def run(self):
        html_template_path =  'blog/newcommentemail.html'
        context = {'name': self.obj.name, 'email': self.obj.email, 'post': self.post.title, 'link': self.link}
        email_html_template = get_template(html_template_path).render(context)
        receiver_email = from_this_email
        email_msg = EmailMessage("New Comment", email_html_template, from_email = from_this_email, to = [receiver_email], reply_to=[from_this_email])
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=True)