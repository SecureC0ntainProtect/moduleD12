from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.core.mail import mail_managers

from .models import Mailing


def notify_managers_appointment(sender, instance, created, **kwargs):
    mail_managers(
        subject=f'{instance.client_name} {instance.date.strftime("%d %m %Y")}',
        message=instance.message,
    )
    print(f'{instance.client_name} {instance.date.strftime("%d %m %Y")}')


post_save.connect(notify_managers_appointment, sender=Mailing)


class MailingView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        mailing = Mailing(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        mailing.save()

        html_content = render_to_string(
            'mailing_created.html',
            {
                'mailing': mailing,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{mailing.client_name} {mailing.date.strftime("%Y-%M-%d")}',
            body=mailing.message,
            from_email='test@mail.com',
            to=['test@mail.com'],
        )
        msg.attach_alternative(html_content, 'text/html')

        msg.send()

        return redirect('mailing:make_mailing')