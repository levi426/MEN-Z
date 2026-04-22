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
    image = serializers.SerializerMethodField()
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
            'image',
            'reviews'
        ]

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_reviews(self, obj):
        reviews = Review.objects.filter(
            product_type='clothing',
            product_id=obj.id
        )
        return ReviewSerializer(reviews, many=True, context=self.context).data


ProductSerializer = ClothingProductSerializer