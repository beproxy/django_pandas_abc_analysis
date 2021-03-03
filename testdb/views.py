import json
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from testdb.calculations import Manipulation
from testdb.models import Sales
from testdb.serializers import QuantitySalesBrandsSerializer, SalesDetailsSerializer, TurnoverBrandsSerializer, \
    AverageCheckStoreSerializer, QuantityChecksBrandSerializer
from django.db.models import F, Sum, Count, DecimalField, ExpressionWrapper
import logging
logger = logging.getLogger('logfile')



def index(request):
    output = {'average_check': "average_check",
              'turnover_brands': "turnover_brands",
              'quantity_sales_brands': "quantity_sales_brands",
              'quantity_checks_brands': "quantity_checks_brands",
              # 'abc_analysis': "abc_analysis"
              }
    return render(request, 'index.html', context=output)


# View class Manipulation with PARAMS
def data_to_csv_view(request):
    manipulation = Manipulation()
    try:
        name_func = request.GET.get('params').strip('/')
    except Exception as err:
        logger.error(f'{err}')
    result = getattr(manipulation, name_func)()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{name_func}.csv"'

    result.to_csv(path_or_buf=response)
    return response


# Sales Details view
class SalesDetailView(APIView):

    def get(self, request, pk):
        try:
            queryset = Sales.objects.get(id=pk)
        except Exception as err:
            logger.error(f'{err}')
        serializer = SalesDetailsSerializer(queryset)
        return Response(serializer.data)


# View Average check for the store
class AverageCheckView(APIView):

    def get(self, request):
        try:
            queryset = Sales.objects.filter(total_price__gte=0) \
                .values(store=F("store__name")) \
                .annotate(avg_sum_check=ExpressionWrapper(
                    Sum(F('total_price')) / Count(F('check_id'), distinct=True),
                    output_field=DecimalField(max_digits=20, decimal_places=2)
                )
            )
        except Exception as err:
            logger.error(f'{err}')
        serializer = AverageCheckStoreSerializer(queryset, many=True)
        return Response(serializer.data)


# View Turnover of brands
class TurnoverBrandsView(APIView):

    def get(self, request):
        try:
            queryset = Sales.objects.filter(total_price__gte=0) \
                .values(store=F("store__name"), brand=F('product__brand__name'))[:10000] \
                .annotate(total_turnover=Sum('total_price'))
        except Exception as err:
            logger.error(f'{err}')
        serializer = TurnoverBrandsSerializer(queryset, many=True)
        return Response(serializer.data)


# View Quantity of sales by brands
class QuantitySalesBrandsView(APIView):

    def get(self, request):
        try:
            queryset = Sales.objects.filter(qty__gte=0) \
                .values(brand=F("product__brand__name")) \
                .annotate(total=Sum('qty'))
        except Exception as err:
            logger.error(f'{err}')
        serializer = QuantitySalesBrandsSerializer(queryset, many=True)
        return Response(serializer.data)


# View Quantity of checks by brand
class QuantityChecksBrandView(APIView):

    def get(self, request):
        try:
            queryset = Sales.objects.filter(total_price__gte=0) \
                .values(brand=F("product__brand__name"))[:10000] \
                .annotate(quantity_checks=Count('check_id'))
        except Exception as err:
            logger.error(f'{err}')
        serializer = QuantityChecksBrandSerializer(queryset, many=True)
        return Response(serializer.data)


# View aggregate data by brands
class AggregateDataBrandsView(APIView):

    def get(self, request):
        manipulation = Manipulation()
        data = manipulation.aggregate_data_brands()
        try:
            parsed = json.loads(data)
        except Exception as err:
            logger.error(f'{err}')
        return Response(parsed)


# View ABC analysis of products by turnover by shop ID or all shops
class AbcAnalysisView(APIView):

    def get(self, request):
        try:
            id = self.request.GET.get('store_id')
        except Exception as err:
            logger.error(f'{err}')
        manipulation = Manipulation()
        if id != None:
            data = manipulation.abc_analysis(id)
            try:
                parsed = json.loads(data)
            except Exception as err:
                logger.error(f'{err}')
            return Response({f'store_{id}': parsed})

        data = manipulation.shops_abc_analysis()
        try:
            parsed = json.loads(data)
        except Exception as err:
            logger.error(f'{err}')
        return Response(parsed)
