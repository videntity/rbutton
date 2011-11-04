#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


LEVEL_CHOICES=(
            ('0','Send All information (not recommended)'),
            ('1','Remove name and contact information'),
            ('2','Also remove family history and military service'),
            ('3','Also remove medications'),)




class UploadForm(forms.Form):
    file  = forms.FileField()


class SelectFilterForm(forms.Form):
    level  = forms.TypedChoiceField(choices= LEVEL_CHOICES,
                                    widget=forms.RadioSelect(),
                                    label="How much of your information do you want to keep private?",
                                    initial="1",)
   
    