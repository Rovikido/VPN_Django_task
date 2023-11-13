from django.contrib.auth.models import User
from django.db import models


class Website(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=500)


# TODO: potentialy allow storage of data per x days for better tracking
class Statistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.OneToOneField(Website, on_delete=models.CASCADE)
    page_views = models.IntegerField(default=0, null=False, validators=[models.MinValueValidator(0)])
