# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import task
from poll.models import Poll
from django.conf import settings
from django.template import loader, Context
from django.core.mail import send_mail, EmailMultiAlternatives

@task()
def send_invitations(poll_uid):
    poll = Poll.objects.get(unique_id=poll_uid)

    t = loader.get_template('email/invitation.html')

    for client in poll.clients.all():
        c = Context({
            'poll': poll,
            'client': client,
            'default_domain': settings.DEFAULT_DOMAIN,
        })
        message = t.render(c)

        msg = EmailMultiAlternatives(poll.title, '', settings.DEFAULT_FROM_EMAIL, [client.email])
        msg.attach_alternative(message, "text/html")
        msg.send()

    poll.is_sent = True

    poll_created_sbj = 'Mail Interview created!'
    poll_created_msg = 'Mail interview "%s" successfully created!\n' \
                       'You can get result by link http://%s/poll/%s/%s/.\n' \
                       'Thank you!\n' \
                       '--\n' \
                       'Best regards,' \
                       'Hosting4Django.net Team' % (poll.title, settings.DEFAULT_DOMAIN, poll.unique_id, poll.secret_key)
    send_mail(
        poll_created_sbj,
        poll_created_msg,
        settings.DEFAULT_FROM_EMAIL,
        [poll.author_email],
        fail_silently=False
    )

    return poll.save()

@task()
def send_results(poll_uid):
    poll = Poll.objects.get(unique_id=poll_uid)
    subject = 'Mail Interview results - "%s"' % poll.title

    if not poll.is_done:
        for client in poll.clients.filter(is_need_res=True):
            print client
            t = loader.get_template('email/results.html')
            c = Context({
                'poll': poll,
                'default_domain': settings.DEFAULT_DOMAIN,
                'variants': poll.variants.order_by('-votes_count'),
                'client': client
                })
            message = t.render(c)

            msg = EmailMultiAlternatives(subject, '', settings.DEFAULT_FROM_EMAIL, [client.email])
            msg.attach_alternative(message, "text/html")
            msg.send()

    poll.is_done = True

    return poll.save()
