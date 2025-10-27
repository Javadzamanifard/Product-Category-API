from rest_framework import serializers

from .models import Category, CustomUser, Product

from django.utils.text import slugify


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = 'auth.User'
        fields = ['id', 'user', 'phone']



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'user', 'phone']



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
        read_only_fields = ['id', 'slug', 'is_active', 'category', 'created_at', ]
    
    
    def validate_price(self, value):
        import decimal
        if not isinstance(value, (int, decimal.Decimal)):
            raise serializers.ValidationError('Price must be a number.')
        if value <= 0: 
            raise serializers.ValidationError('Price must be a positive number.')
        return value
    
    def validate_stock(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError('stock must be an integer number.')
        if value < 0:
            raise serializers.ValidationError('Stock cannot be negative.')
        return value
    
    def validate(self, data):
        stock = data.get('stock')
        is_active = data.get('is_active', False)
        if stock == 0 and is_active is True:
            raise serializers.ValidationError('A product with zero stock cannot be active.')
        return data
    
    
    # ---------------------------
    # 🔹 Create method
    # ---------------------------
    def create(self, validated_data):
        name = validated_data.get('name')
        slug = slugify(name)
        if Product.objects.filter(slug=slug).exists():
            raise serializers.ValidationError({'name': 'A product with this name already exists.'})
        validated_data['slug'] = slugify(name)
        product = Product.objects.create(**validated_data)
        return product
    
    
    # ---------------------------
    # 🔹 Update method
    # ---------------------------
    def update(self, instance, validated_data):
        new_name = validated_data.get('name')
        if new_name and new_name != instance.name:
            validated_data['slug'] = slugify(new_name)
        return super().update(instance, validated_data)