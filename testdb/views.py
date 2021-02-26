import json

from django.db.models import Sum
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
from testdb.serializers import QuantitySalesBrandsSerializer, ProductSaleDetailsSerializer, ProductDetailsSerializer
from django.db.models import F


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
        queryset = DataProductsale.objects.get(id=pk)
        qs = DataProduct.objects.get(id='23470')
        sr = ProductDetailsSerializer(qs)
        print(sr.data)
        serializer = ProductSaleDetailsSerializer(queryset)
        return Response(serializer.data)


# View Average check for the store
class AverageCheckView(APIView):

    def get(self, request, format=None):
        manipulation = Manipulation()
        data = manipulation.average_check()
        parsed = json.loads(data)
        return Response(parsed)


# View Turnover of brands
class TurnoverBrandsView(APIView):

    def get(self, request, format=None):
        manipulation = Manipulation()
        data = manipulation.turnover_brands()
        parsed = json.loads(data)
        return Response(parsed)


# View Quantity of sales by brands
class QuantitySalesBrandsView(APIView):

    def get(self, request):
        qs = DataProductsale.objects.filter(qty__gte=0).values(brand=F("product__brand__name")) \
            .annotate(total=Sum('qty'))
        serializer = QuantitySalesBrandsSerializer(qs, many=True)
        return Response(serializer.data)


# View Quantity of receipts by brands
class QuantityReceiptsBrandsView(APIView):

    def get(self, request, format=None):
        manipulation = Manipulation()
        data = manipulation.quantity_receipts_brands().to_json()
        parsed = json.loads(data)
        return Response(parsed)

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
