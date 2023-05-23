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
                                  verbose_name="Nome",
                                  unique=True)
    serie_number = models.CharField(max_length=120, null=True, blank=True,
                                    verbose_name="Número de série",
                                    unique=True)
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
                                   verbose_name="Nome",
                                   unique=True)
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
                                  auto_now_add=True,
                                  verbose_name="Data de início")
    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name        = 'Aluguer'
        verbose_name_plural = 'Alugueres'

class PlaceCategory(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True,
                            verbose_name="Nome")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = 'Categoria de local'
        verbose_name_plural = 'Categorias de local'

class Place(models.Model):
    name       = models.CharField(max_length=120, null=True, blank=True,
                                  verbose_name="Nome",
                                  unique=True)
    category   = models.ForeignKey(PlaceCategory, null=True, blank=True,
                                   verbose_name="Categoria",
                                   on_delete=models.CASCADE)
    description = models.CharField(max_length=120, null=True, blank=True,
                                      verbose_name="Descrição")
    lat = models.CharField(max_length=120, null=True, blank=True,
                                      verbose_name="Latitude")
    lng = models.CharField(max_length=120, null=True, blank=True,
                                        verbose_name="Longitude")
    image = ResizedImageField(size=[500, 300], null=True, blank=True,
                              quality=100, upload_to='images/places/',
                              force_format='WEBP', keep_meta=False,
                              verbose_name="Imagem")
    @property
    def image_url(self):
        return "{0}{1}".format(settings.SITE_URL, self.image.url)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = 'Local'
        verbose_name_plural = 'Locais'
