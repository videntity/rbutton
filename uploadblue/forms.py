#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


LEVEL_CHOICES=(
            ('0','Send All information (not reccomended)'),
            ('1','Remove name and contact information'),
            ('2','Also remove family history and military service'),
            ('3','Also remove medications'),)




class UploadForm(forms.Form):
    file  = forms.FileField()


class SelectFilterForm(forms.Form):
    level  = forms.TypedChoiceField(choices= LEVEL_CHOICES,
                                    widget=forms.RadioSelect(),
                                    label="Select your filter level",
                                    initial="1",)
    national_cancer_institute   = forms.BooleanField(initial=True)
    novartis                    = forms.BooleanField(initial=True)
    world_health_organization   = forms.BooleanField(initial=True)
    center_for_disease_control  = forms.BooleanField(initial=True)
    