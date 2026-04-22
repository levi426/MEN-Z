from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'order',
            'user',
            'image',   # ✅ FIXED (was screenshot)
            'uploaded_at',
            'status'
        ]
        read_only_fields = ('id', 'user', 'uploaded_at')