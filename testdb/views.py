from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from testdb.calculations import Manipulation



def index(request):
    output = {'average_check': "average_check",
              'turnover_brands': "turnover_brands",
              'quantity_sales_brands': "quantity_sales_brands",
              'quantity_receipts_brands': "quantity_receipts_brands",
              'abc_analysis': "abc_analysis"}
    return render(request, 'index.html', context=output)


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
