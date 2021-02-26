from rest_framework import serializers

from testdb.models import DataProductsale, DataProduct, DataBrand, DataShop


class QuantitySalesBrandsSerializer(serializers.Serializer):
    brand = serializers.CharField(max_length=150)
    total = serializers.DecimalField(max_digits=20, decimal_places=4)

    class Meta:
        model = DataProductsale
        fields = ('brand', 'total')


class ProductSaleDetailsSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field="name", read_only=True)
    shop = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = DataProductsale
        fields = '__all__'


# Product Details
class ProductDetailsSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = DataProduct
        fields = '__all__'


# Brand Details
class BrandDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataBrand
        fields = ('name',)


# Shop Details
class ShopDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataShop
        fields = ('name',)