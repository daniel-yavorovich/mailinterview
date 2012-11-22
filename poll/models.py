# -*- coding: utf-8 -*-
from django.db import models
from poll.fields import UUIDField

class Client(models.Model):
    unique_id   = UUIDField(primary_key=True, editable=False)
    email       = models.EmailField()
    is_need_res = models.BooleanField(default=False, blank=True)
    is_voted    = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return self.email

class Variant(models.Model):
    name        = models.CharField(max_length=300)
    votes_count = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        return self.name

class Poll(models.Model):
    unique_id   = UUIDField(primary_key=True, editable=False)
    is_open     = models.BooleanField(default=True, blank=True)
    title       = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    variants    = models.ManyToManyField(Variant)
    clients     = models.ManyToManyField(Client)
    author_email= models.EmailField()
    author_name = models.CharField(max_length=300)
    is_sent     = models.BooleanField(default=False, blank=True)
    is_done     = models.BooleanField(default=False, blank=True)
    secret_key  = UUIDField(editable=False)

    def __unicode__(self):
        return self.title