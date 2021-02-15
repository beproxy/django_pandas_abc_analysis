from testdb.models import DataProductsale
import pandas as pd


class Manipulation:
    # Average check for the store
    def average_check(self):
        try:
            qs = DataProductsale.objects.filter(total_price__gte=0).values('total_price', "shop__name")
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        df.total_price = pd.to_numeric(df["total_price"])
        return df.groupby("shop__name").total_price.mean()

    # Turnover of brands
    def turnover_brands(self):
        try:
            qs = DataProductsale.objects.filter(total_price__gte=0).values('total_price', 'product__brand__name')
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        return df.groupby(['product__brand__name']).sum()

    # Quantity of sales by brands
    def quantity_sales_brands(self):
        try:
            qs = DataProductsale.objects.filter(qty__gte=0).values('qty', "product__brand__name")
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        return df.groupby(['product__brand__name']).sum()

    # Quantity of receipts by brands
    def quantity_receipts_brands(self):
        try:
            qs = DataProductsale.objects.filter(total_price__gte=0).values('receipt_id', "product__brand__name")
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        return df.groupby(['product__brand__name']).size()

    # Withdraw Group A goods by turnover (ABC analysis)
    def abc_analysis(self):
        try:
            qs = DataProductsale.objects.filter(margin_price_total__gte=0).values('margin_price_total', "product", "shop__name")
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        df = df.groupby(['product', "shop__name"]).sum()
        total_margin_shop = df.drop(['product'], axis=1)
        df['total_margin_shop'] = df.groupby(["shop__name"]).margin_price_total.sum()

        df.margin_price_total = df.margin_price_total * 100 / total_margin_shop[df[df.shop__name]]
        # df.sort_values(by='margin_price_total', ascending=False)
        return df