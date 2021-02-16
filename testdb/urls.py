from django.urls import include, path, re_path
from testdb import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.data_to_csv_view, name='data_to_csv'),
    path('api/brand/average_check/', views.AverageCheckView.as_view(), name='average_check_view'),
    path('api/brand/turnover/', views.TurnoverBrandsView.as_view(), name='turnover_brands_view'),
    path('api/brand/quantity_sales/', views.QuantitySalesBrandsView.as_view(), name='quantity_sales_brands_view'),
    path('api/brand/quantity_receipts/', views.QuantityReceiptsBrandsView.as_view(), name='quantity_receipts_brands_view'),
    path('api/brand/abc_analysis/', views.AbcAnalysisView.as_view(), name='abc_analysis_view'),
]
