from rest_framework import serializers
from .models import Pet, PetType


# --- Define PetTypeSerializer first ---
class PetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetType
        fields = '__all__'


# --- Then define PetSerializer ---
class PetSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    modified_by = serializers.ReadOnlyField(source='modified_by.username')
    image = serializers.ImageField(required=False, allow_null=True)

    # Show full PetType details (nested)
    pet_type = PetTypeSerializer(read_only=True)

    # Allow assigning pet_type by ID when creating/updating
    pet_type_id = serializers.PrimaryKeyRelatedField(
        queryset=PetType.objects.all(),
        source='pet_type',
        write_only=True,
        required=False
    )

    image = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ("id", "created_by", "created_date")

    # --- Custom field validations ---
    def validate_age(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Age must be 0 or greater.")
        return value

    def validate_weight(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Weight must be 0 or greater.")
        return value

    def validate_pincode(self, value):
        if value is not None:
            s = str(value)
            if len(s) < 3 or len(s) > 10:
                raise serializers.ValidationError("Pincode looks invalid.")
        return value

    # --- Handle image absolute URL ---
    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            try:
                return request.build_absolute_uri(obj.image.url)
            except Exception:
                return obj.image.url
        return None
