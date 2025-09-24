# backend/users/models.py

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(blank=True, verbose_name="Número de Telefone")
    country = CountryField(blank=True, verbose_name="País")

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Este "sinal" garante que um Perfil é criado automaticamente sempre que um Utilizador é criado.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()