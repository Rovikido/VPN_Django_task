from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator


class Website(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=500)


# TODO: potentialy allow storage of data per x days for better tracking
class Statistics(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    website = models.OneToOneField(Website, null=False, on_delete=models.CASCADE)
    page_views = models.IntegerField(default=0, null=False, validators=[MinValueValidator(0)])
    data_transferred = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False, validators=[MinValueValidator(0)]) # stored in MB
