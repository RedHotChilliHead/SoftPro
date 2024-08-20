from django.db import models


class Baseball(models.Model):
    class Meta:
        ordering = ['id']

    # CHOICE_VERSION = [
    #     ('full', 'Full'),
    #     ('delta', 'Delta'),
    # ]
    # version = models.CharField(max_length=5, choices=CHOICE_VERSION, blank=False, null=False)
    line = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    date = models.DateField(blank=False, null=False, auto_now_add=True)


class Football(models.Model):
    class Meta:
        ordering = ['id']

    # CHOICE_VERSION = [
    #     ('full', 'Full'),
    #     ('delta', 'Delta'),
    # ]
    # version = models.CharField(max_length=5, choices=CHOICE_VERSION, blank=False, null=False)
    line = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    date = models.DateField(blank=False, null=False, auto_now_add=True)


class Soccer(models.Model):
    class Meta:
        ordering = ['id']

    # CHOICE_VERSION = [
    #     ('full', 'Full'),
    #     ('delta', 'Delta'),
    # ]
    # version = models.CharField(max_length=5, choices=CHOICE_VERSION, blank=False, null=False)
    line = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    date = models.DateField(blank=False, null=False, auto_now_add=True)
