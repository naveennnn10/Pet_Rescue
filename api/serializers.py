from rest_framework import serializers
from .models import Pet, PetType

class PetSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    modified_by = serializers.ReadOnlyField(source='modified_by.username')
    pet_type = serializers.PrimaryKeyRelatedField(queryset=PetType.objects.all())
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ("id", "created_by", "created_date")

    # Simple field validation examples:
    def validate_age(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Age must be 0 or greater.")
        return value

    def validate_weight(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Weight must be 0 or greater.")
        return value

    def validate_pincode(self, value):
        # change rules to match your country format
        if value is not None:
            s = str(value)
            if len(s) < 3 or len(s) > 10:
                raise serializers.ValidationError("Pincode looks invalid.")
        return value