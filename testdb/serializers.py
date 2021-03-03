from rest_framework import serializers

from testdb.models import Sales, Product, Brand, Store



class SalesDetailsSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field="name", read_only=True)
    shop = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Sales
        fields = '__all__'


# Product Details
class ProductDetailsSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


# Brand Details
class BrandDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('name',)


# Store Details
class StoreDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ('name',)


# Serializer Quantity of sales by brands
class QuantitySalesBrandsSerializer(serializers.Serializer):
    brand = serializers.CharField(max_length=150)
    total = serializers.DecimalField(max_digits=20, decimal_places=4)

    class Meta:
        model = Sales
        fields = ('brand', 'total')


# Serializer turnover of brands
class TurnoverBrandsSerializer(serializers.Serializer):
    store = serializers.CharField(max_length=150)
    brand = serializers.CharField(max_length=150)
    total_turnover = serializers.DecimalField(max_digits=20, decimal_places=4)

    class Meta:
        model = Sales
        fields = ('store', 'brand', 'total_turnover')


# Serializer Average check for the store
class AverageCheckStoreSerializer(serializers.Serializer):
    store = serializers.CharField(max_length=150)
    avg_sum_check = serializers.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        model = Sales
        fields = ('store', 'avg_sum_check')


# Serializer Quantity of checks by brands
class QuantityChecksBrandSerializer(serializers.Serializer):
    brand = serializers.CharField(max_length=150)
    quantity_checks = serializers.IntegerField()

    class Meta:
        model = Sales
        fields = ('brand', 'quantity_checks')

