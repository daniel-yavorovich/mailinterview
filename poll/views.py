# -*- coding: utf-8 -*-
from django.conf import settings
from poll.forms import LaunchPollForm
from django.template import RequestContext
from django.core.urlresolvers import reverse
from poll.models import Poll, Variant, Client
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from poll.tasks import send_invitations, send_results
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    return render_to_response('index.html',
        {
            'default_domain': settings.DEFAULT_DOMAIN,
        },
        context_instance=RequestContext(request)
    )

def launch(request):
    if request.method == 'POST':
        form = LaunchPollForm(request.POST)
        if form.is_valid():
            poll = Poll.objects.create(
                title       = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                author_name = form.cleaned_data['author_name'],
                author_email= form.cleaned_data['author_email'],
            )

            for var in form.cleaned_data['variants']:
                variant = Variant.objects.create(name=var)
                poll.variants.add(variant)

            for email in form.cleaned_data['emails']:
                client = Client.objects.create(email=email)
                poll.clients.add(client)

            poll.save()

            send_invitations.delay(poll.unique_id)

            return HttpResponseRedirect(reverse('poll', args=(poll.unique_id, poll.secret_key)))
    else:
        form = LaunchPollForm()

    return render_to_response('launch.html',
        {
            'form': form,
            'default_domain': settings.DEFAULT_DOMAIN,
        },
        context_instance=RequestContext(request)
    )

def poll(request, poll_id, secret_key):
    poll = get_object_or_404(Poll, unique_id = poll_id, secret_key = secret_key)

    return render_to_response('poll.html',
        {
            'poll': poll,
            'default_domain': settings.DEFAULT_DOMAIN,
            'variants': poll.variants.order_by('-votes_count'),
            'voted_users': poll.clients.filter(is_voted=True),
            'signed_users': poll.clients.filter(is_need_res=True),
        },
        context_instance=RequestContext(request)
    )

def vote(request, poll_id, client_id, var_id):
    poll = get_object_or_404(Poll, unique_id = poll_id)
    client = get_object_or_404(poll.clients, pk = client_id)
    var = get_object_or_404(poll.variants, pk = var_id)

    if client.is_voted:
        message = "You already vote!"
    else:
        # Increment variant votes
        var.votes_count += 1
        var.save()

        # Mark client as voted
        client.is_voted = True
        client.save()
        message = "Thank you for you vote!"

    return render_to_response('vote.html',
        {
            'poll': poll,
            'client': client,
            'message': message,
            'default_domain': settings.DEFAULT_DOMAIN,
        },
        context_instance=RequestContext(request)
    )

def stop_interview(request, poll_uid, secret_key):
    poll = get_object_or_404(Poll, unique_id = poll_uid, secret_key = secret_key)
    if not poll.is_done:
        send_results.delay(poll_uid)
        result = "OK"
    else:
        result = "Interview already stopped"

    return HttpResponse(result)

def signup_results(request, poll_uid, client_uid):
    poll = get_object_or_404(Poll, unique_id = poll_uid)
    client = get_object_or_404(poll.clients, unique_id = client_uid)
    client.is_need_res = True
    client.save()

    return HttpResponse("OK")

def show_results(request, poll_id, client_uid):
    poll = get_object_or_404(Poll, unique_id = poll_id)
    client = get_object_or_404(poll.clients, unique_id = client_uid)

    return render_to_response('results.html',
        {
            'poll': poll,
            'client': client,
            'default_domain': settings.DEFAULT_DOMAIN,
            'variants': poll.variants.order_by('-votes_count'),
            'voted_users': poll.clients.filter(is_voted=True),
            'signed_users': poll.clients.filter(is_need_res=True),
        },
        context_instance=RequestContext(request)
    )
