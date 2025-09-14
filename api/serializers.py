from rest_framework import serializers
from .models import Pet

class PetSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    modified_by = serializers.ReadOnlyField(source='modified_by.username')

    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ('created_by', 'modified_by', 'created_date', 'modified_date')
