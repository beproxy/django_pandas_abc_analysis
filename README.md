# Test project
Used Python 3.6, Django 2.2.5, DRF, ORM, Pandas, Logging

Tasks
```
Aggregate, calculations of data from DB (PostgreSQL)

Output:
 As file csv
 DRF render json: use ORM and Pandas
```

Endpoints

```
'' - html home page with link to save data to CSV file (use pandas)

Use ORM 
'api/brand/average_check/' - Average check for the store
'api/brand/turnover/' - Turnover of brands
'api/brand/quantity_sales/' - Quantity of sales by brands
'api/brand/quantity_checks/' - Quantity of checks by brand

Use Pandas
'api/brand/abc_analysis/?store_id=<int:id>' - ABC analysis of products by turnover by the store ID
'api/brands/aggregate_data/' - ABC analysis of products by turnover by the all stores
```

