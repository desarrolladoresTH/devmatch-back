from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import threading

class Util:
    @staticmethod #no necesita un self
    def send_email(data):
        
        
         html_content = render_to_string("password_reset.html",{'context':data['email_body'],'context1':data['codigo1'],'context2':data['codigo2']})
         text_content= strip_tags(html_content)
         email=  EmailMessage(
            subject=data['email_subject'],
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[data['to_email']]
         )
         email.attach_alternative(html_content,"text/html")
 
         email.send()

    
    def send_email2(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()