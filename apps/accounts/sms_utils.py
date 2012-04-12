#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from twilio.rest import TwilioRestClient


def send_sms_twilio(twilio_body, twilio_to,
                    twilio_from=settings.TWILIO_DEFAULT_FROM):
    
    client = TwilioRestClient(settings.TWILIO_SID,settings.TWILIO_AUTH_TOKEN)

    d = {
    'From' : twilio_from,
    'To' : twilio_to,
    'Body': twilio_body
    }
    
    x = client.sms.messages.create(from_=twilio_from,
                                       to=twilio_to,
                                       body=twilio_body)
    return x


