from rest_framework import serializers

from testdb.models import DataProductsale, DataProduct


class QuantitySalesBrandsSerializer(serializers.ModelSerializer):
#    qty = serializers.DecimalField(max_digits=20, decimal_places=4)
    product = serializers.RelatedField(read_only=True)

    class Meta:
        model = DataProductsale
        fields = ('qty', 'product')


class DataProductsSerializer(serializers.ModelSerializer):
#    qty = serializers.DecimalField(max_digits=20, decimal_places=4)
    brands = QuantitySalesBrandsSerializer(read_only=True)

    class Meta:
        model = DataProduct
        fields = ('brand_product')