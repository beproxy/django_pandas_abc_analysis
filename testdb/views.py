import json

from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from settings import settings
from testdb.calculations import Manipulation
from testdb.models import DataProductsale, DataCategory, DataProduct
from testdb.serializers import QuantitySalesBrandsSerializer, ProductSaleDetailsSerializer, ProductDetailsSerializer, \
    TurnoverBrandsSerializer, AverageCheckStoreSerializer, QuantityChecksBrandSerializer
from django.db.models import F, Avg, Sum, Count, DecimalField, ExpressionWrapper


def index(request):
    output = {'average_check': "average_check",
              'turnover_brands': "turnover_brands",
              'quantity_sales_brands': "quantity_sales_brands",
              'quantity_receipts_brands': "quantity_receipts_brands",
              # 'abc_analysis': "abc_analysis"
              }
    return render(request, 'index.html', context=output)


# View class Manipulation with PARAMS
def data_to_csv_view(request):
    manipulation = Manipulation()
    try:
        name_func = request.GET.get('params').strip('/')
    except Exception as err:
        print(err)
    result = getattr(manipulation, name_func)()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{name_func}.csv"'

    result.to_csv(path_or_buf=response)
    return response


# Product Sale Details view
class ProductSaleDetailView(APIView):

    def get(self, request, pk):
        try:
            queryset = DataProductsale.objects.get(id=pk)
        except Exception as err:
            print(err)
        serializer = ProductSaleDetailsSerializer(queryset)
        return Response(serializer.data)


# View Average check for the store
class AverageCheckView(APIView):

    def get(self, request, format=None):
        try:
            queryset = DataProductsale.objects.filter(total_price__gte=0) \
                .values(store=F("shop__name"))[:10000] \
                .annotate(avg_sum_check=ExpressionWrapper(
                    Sum(F('total_price')) / Count(F('receipt_id'), distinct=True),
                    output_field=DecimalField(max_digits=20, decimal_places=2)
                )
            )
        except Exception as err:
            print(err)
        serializer = AverageCheckStoreSerializer(queryset, many=True)
        return Response(serializer.data)


# View Turnover of brands
class TurnoverBrandsView(APIView):

    def get(self, request, format=None):
        try:
            queryset = DataProductsale.objects.filter(total_price__gte=0) \
                .values(store=F("shop__name"), brand=F('product__brand__name'))[:10000] \
                .annotate(total_turnover=Sum('total_price'))
        except Exception as err:
            print(err)
        serializer = TurnoverBrandsSerializer(queryset, many=True)
        return Response(serializer.data)


# View Quantity of sales by brands
class QuantitySalesBrandsView(APIView):

    def get(self, request):
        try:
            queryset = DataProductsale.objects.filter(qty__gte=0) \
                .values(brand=F("product__brand__name")) \
                .annotate(total=Sum('qty'))
        except Exception as err:
            print(err)
        serializer = QuantitySalesBrandsSerializer(queryset, many=True)
        return Response(serializer.data)


# View Quantity of checks by brands
class QuantityReceiptsBrandsView(APIView):

    def get(self, request, format=None):
        try:
            queryset = DataProductsale.objects.filter(total_price__gte=0) \
                .values(brand=F("product__brand__name"))[:10000] \
                .annotate(quantity_checks=Count('receipt_id'))
        except Exception as err:
            print(err)
        serializer = QuantityChecksBrandSerializer(queryset, many=True)
        return Response(serializer.data)


# View aggregate data by brands
class AggregateDataBrandsView(APIView):

    def get(self, request, format=None):
        manipulation = Manipulation()
        data = manipulation.aggregate_data_brands()
        parsed = json.loads(data)
        return Response(parsed)


# View ABC analysis of products by turnover by shop ID or all shops
class AbcAnalysisView(APIView):

    def get(self, request, format=None):
        try:
            id = self.request.GET.get('shop_id')
        except Exception as err:
            print(err)
        manipulation = Manipulation()
        if id != None:
            data = manipulation.abc_analysis(id)
            parsed = json.loads(data)
            return Response({f'shop_{id}': parsed})

        data = manipulation.shops_abc_analysis()
        parsed = json.loads(data)
        return Response(parsed)
