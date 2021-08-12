from rest_framework import serializers
from .models import Person


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'age', 'birth_date', 'sex']
