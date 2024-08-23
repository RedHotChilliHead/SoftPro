from django.db import models


class Baseball(models.Model):
    """
    Определение модели спорта - бейсбол
    """
    class Meta:
        ordering = ['id']

    line = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    date = models.DateField(blank=False, null=False, auto_now_add=True)


class Football(models.Model):
    """
    Определение модели спорта - американский футбол
    """
    class Meta:
        ordering = ['id']

    line = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    date = models.DateField(blank=False, null=False, auto_now_add=True)


class Soccer(models.Model):
    """
    Определение модели спорта - футбол
    """
    class Meta:
        ordering = ['id']

    line = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    date = models.DateField(blank=False, null=False, auto_now_add=True)
