#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from django.contrib.localflavor.us.models import PhoneNumberField

import string
import random
import uuid

 
USER_TYPE_CHOICES =          (('organization',  'Organization'),)

ORGANIZATION_CHOICES= ( ('non-profit',  'Non-Profit'),
                         ('for-profit',  'For Profit'),)

APPROVAL_CHOICES =( ('pending',  'Pending'),
                         ('approved',  'Approved'),
                         ('rejected',  'rejected'))



class Organization(models.Model):
    organization_name           = models.CharField(blank= True, max_length=100)
    organization_contact        = models.CharField(blank = True, max_length=100)
    organization_url            = models.URLField(blank = True)
    organization_email          = models.EmailField(blank=True, max_length=100)
    organizaton_linked_owner    = models.ForeignKey(User, blank=True, null=True, unique=True)
    user_type                   = models.CharField(max_length=20,
                                               choices=USER_TYPE_CHOICES, default='Organization')                                            
    organization_type           = models.CharField(max_length=20, choices=ORGANIZATION_CHOICES)
    approval_status             = models.CharField(max_length=10,
                                               choices=APPROVAL_CHOICES,
                                               default='pending')
    phone_number                = PhoneNumberField(max_length=15) 
    twitter                     = models.CharField(blank = True, max_length=15)
    notes                       = models.CharField(blank = True, max_length=250)
        
    class Meta:
        unique_together = (("organization_name", "organization_type"),)

    def __unicode__(self):
            return '%s is a %s entity' % (self.organization_name, self.organization_type)