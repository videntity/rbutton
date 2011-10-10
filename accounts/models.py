from django.db import models
from django.contrib.auth.models import User
from datetime import date

gender_choices=(
        ('female','female'),
        ('male','male'),
        )

annon_choices=(
        ('Public','Public'),
        ('Anonymous','Anonymous'),
        )



i=24
hc_list=[]
while i < 96:
     ft=i/12
     ft_in="%sft. %sin." %(i/12,i%12)
     choice=(i, ft_in)
     hc_list.append(choice)
     i=i+1
height_choices=tuple(hc_list)


class UserProfile(models.Model):
    user  = models.ForeignKey(User, unique=True)
    #display_name = models.CharField(max_length=30, blank=True)
    coach = models.BooleanField(default=False)
    initpbf = models.FloatField(default=0.0, blank=True)
    studentid = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=40, choices=gender_choices)
    height_in = models.IntegerField(max_length=4)
    pin = models.IntegerField(max_length=4)
    birthdate = models.DateField(default=date.today())
    mobile_phone_number = models.CharField(max_length=15, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    steps_per_day_goal = models.IntegerField(max_length=7, default=10000, blank=True)
    weight_goal = models.IntegerField(max_length=4, default=0)
    annon = models.CharField(max_length=100, choices=annon_choices)

    def __unicode__(self):
        return 'profile for %s %s %s %s' % (self.user.username, self.user.email,
                                   self.user.first_name,
                                   self.user.last_name)
