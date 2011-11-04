from django.db import models


class BlueButtonFileUpload(models.Model):
    file    = models.FileField(upload_to="bluebutton__original_files/")

