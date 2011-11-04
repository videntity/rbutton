#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from models import BlueButtonFileUpload

LEVEL_CHOICES=(
            ('0','Send All information (not recommended)'),
            ('1','Remove name and contact information'),
            ('2','Also remove family history and military service'),
            ('3','Also remove medications'),)



FATIGUE_CHOICES=(
            ('0','Not at all'),
            ('1','A little'),
            ('2','Somewhate'),
            ('3','All the times'),)


class BlueButtonFileUploadForm(forms.ModelForm):
    class Meta:
        model = BlueButtonFileUpload


class SelectFilterForm(forms.Form):
    level  = forms.TypedChoiceField(choices= LEVEL_CHOICES,
                                    widget=forms.RadioSelect(),
                                    label="Select your filter level",
                                    initial="1",)


class DonateForm(forms.Form):        
    national_cancer_institute   = forms.BooleanField(initial=True)
    novartis                    = forms.BooleanField(initial=True)
    world_health_organization   = forms.BooleanField(initial=True)
    center_for_disease_control  = forms.BooleanField(initial=True)
    
class NovartisForm(forms.Form):
    fatigue  = forms.TypedChoiceField(choices= FATIGUE_CHOICES,
                                    widget=forms.RadioSelect(),
                                    label="How much, if at all, does this drug make you fatigued?")

class SubmitDataRecipientRequestForm(forms.Form):
    organization_name           = forms.CharField(max_length=100)
    organization_representative = forms.CharField(max_length=100)
    organization_email          = forms.EmailField()
    organization_phone          = forms.CharField(max_length=20)

