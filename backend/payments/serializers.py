from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'order',
            'user',
            'image',
            'uploaded_at',
            'status'
        ]
        read_only_fields = ('id', 'user', 'uploaded_at')