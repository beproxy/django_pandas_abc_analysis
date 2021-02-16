import json

from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from testdb.calculations import Manipulation



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


# View Average check for the store
class AverageCheckView(APIView):
    # renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        manipulation = Manipulation()
        data = manipulation.average_check().to_json()
        parsed = json.loads(data)
        return Response(parsed)

# View Turnover of brands
class TurnoverBrandsView(APIView):

    def get(self, request, format=None):
        manipulation = Manipulation()
        data = manipulation.turnover_brands().to_json()
        parsed = json.loads(data)
        return Response(parsed)

# View Quantity of sales by brands
class QuantitySalesBrandsView(APIView):

    def get(self, request, format=None):
        manipulation = Manipulation()
        data = manipulation.quantity_sales_brands().to_json()
        parsed = json.loads(data)
        return Response(parsed)

# View Quantity of receipts by brands
class QuantityReceiptsBrandsView(APIView):

    def get(self, request, format=None):
        manipulation = Manipulation()
        data = manipulation.quantity_receipts_brands().to_json()
        parsed = json.loads(data)
        return Response(parsed)

# View ABC analysis a product by turnover by the shop ID
class AbcAnalysisView(APIView):

    def get(self, request, format=None):
        id = self.request.GET.get('shop_id')
        manipulation = Manipulation()
        data = manipulation.abc_analysis(id).to_json()
        parsed = json.loads(data)
        return Response({f'shop_{id}': parsed})
