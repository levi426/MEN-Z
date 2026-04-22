from rest_framework import serializers
from .models import ClothingProduct, Review


class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'user_email',
            'product_type',
            'product_id',
            'rating',
            'comment',
            'created_at'
        ]
        read_only_fields = ['user']


class ClothingProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = ClothingProduct
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
            'category',
            'image',   # ✅ This will now return Cloudinary URL automatically
            'reviews'
        ]

    def get_reviews(self, obj):
        reviews = Review.objects.filter(
            product_type='clothing',
            product_id=obj.id
        )
        return ReviewSerializer(reviews, many=True, context=self.context).data


# Optional alias
ProductSerializer = ClothingProductSerializer