# backend/users/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
# ... UserSerializer ...

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    # Adiciona os novos campos do perfil
    phone_number = PhoneNumberField()
    country = CountryField()

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2", "phone_number", "country"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def save(self):
        # Extrai os dados do perfil antes de criar o utilizador
        profile_data = {
            'phone_number': self.validated_data.pop('phone_number'),
            'country': self.validated_data.pop('country')
        }

        user = User(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})

        user.set_password(password)
        user.save()

        # Atualiza o perfil do utilizador com os dados extra
        Profile.objects.update_or_create(user=user, defaults=profile_data)

        return user