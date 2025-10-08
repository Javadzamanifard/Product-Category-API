from rest_framework import serializers

from models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = '__all__'
        read_only_fields = ['id', ]


class ProductSerializer(serializers.ModelSerializer):
    # Read only category
    category = CategorySerializer(read_only=True)
    
    # Write only category 
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        write_only = True,
        source = 'category'
    )
    
    class Meta:
        model  = Product
        fields = ['id', 'name', 'price', 'slug', 'stock', 'is_active', 'category', 'category_id', 'created_at']
        read_only_fields = ['id', 'slug', 'is_active', 'category_id', 'created_at', ]
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be a positive number.')
        return value
    
    def validate(self, data):
        if data['stock'] == 0 and data.get('is_active') is True:
            raise serializers.ValidationError('A product with zero stock cannot be active.')
        return data
