from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.conf import settings
# Create your models here.

"""
User extra data(contacts) i am using english name variables
and on verbose name i am using Portuguese
First Name, Last Name and e-mail are included on User Model
The funds field is the monetary is the value that user has
put on the app
"""
class Profile(models.Model):
    user     = models.OneToOneField(User, null=False, blank=False, verbose_name="Utilizador",
                                on_delete=models.CASCADE)
    address  = models.CharField(max_length=150, null=True, blank=True,
                                verbose_name="Morada")
    zip_code = models.CharField(max_length=12, null=True, blank=True,
                                verbose_name="Código Postal")
    location = models.CharField(max_length=120, null=True, blank=True,
                                verbose_name="Localização")
    phone    = models.IntegerField(null=True, blank=True,
                                   verbose_name="Número de contato")
    funds    = models.FloatField(null=True, blank=True, verbose_name="Fundos")

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name        = 'Perfil'
        verbose_name_plural = 'Perfis'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Bike(models.Model):
    name       = models.CharField(max_length=120, null=True, blank=True,
                                  verbose_name="Nome")
    serie_number = models.CharField(max_length=120, null=True, blank=True,
                                    verbose_name="Número de série")
    status    = models.CharField(max_length=120, null=True, blank=True,
                                 verbose_name="Estado")
    bought    = models.DateField(null=True, blank=True,
                                verbose_name="Data de compra")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = 'Bicicleta'
        verbose_name_plural = 'Bicicletas'

class Plan(models.Model):
    name        = models.CharField(max_length=120, null=True, blank=True,
                                   verbose_name="Nome")
    description = models.CharField(max_length=120, null=True, blank=True,
                                   verbose_name="Descrição")
    price       = models.FloatField(null=True, blank=True,
                                    verbose_name="Preço")
    duration    = models.IntegerField(null=True, blank=True,
                                        verbose_name="Duração")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = 'Plano'
        verbose_name_plural = 'Planos'

class Rent(models.Model):
    user       = models.ForeignKey(User, null=True, blank=True,
                                      verbose_name="Utilizador",
                                        on_delete=models.CASCADE)
    bike       = models.ForeignKey(Bike, null=True, blank=True,
                                        verbose_name="Bicicleta",
                                        on_delete=models.CASCADE)
    plan       = models.ForeignKey(Plan, null=True, blank=True,
                                        verbose_name="Plano",
                                        on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True,
                                        verbose_name="Data de início")
    end_date   = models.DateField(null=True, blank=True,
                                        verbose_name="Data de fim")
    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name        = 'Aluguer'
        verbose_name_plural = 'Alugueres'
