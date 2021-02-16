from testdb.models import DataProductsale
import pandas as pd


class Manipulation:

    @staticmethod
    def abc_segmentation(percent):
        if percent > 0 and percent < 0.8:
            return 'A'
        elif percent >= 0.8 and percent < 0.95:
            return 'B'
        elif percent >= 0.95:
            return 'C'

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
        return df.groupby(['product__brand__name']).total_price.sum()

    # Quantity of sales by brands
    def quantity_sales_brands(self):
        try:
            qs = DataProductsale.objects.filter(qty__gte=0).values('qty', "product__brand__name")
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        return df.groupby(['product__brand__name']).qty.sum()

    # Quantity of receipts by brands
    def quantity_receipts_brands(self):
        try:
            qs = DataProductsale.objects.filter(total_price__gte=0).values('receipt_id', "product__brand__name")
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        return df.groupby(['product__brand__name']).size()

    # ABC analysis a product by turnover by the shop ID
    def abc_analysis(self, id):
        try:
            qs = DataProductsale.objects.filter(shop_id=id, total_price__gte=0).values('total_price', "product")
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        df = df.groupby(['product']).total_price.sum()
        df = df.to_frame()
        df = df.rename(columns={'total_price': "turnover"})
        df = df.sort_values(by='turnover', ascending=False)
        df['cum_sum'] = df['turnover'].cumsum()
        df['total_sum'] = df['turnover'].sum()
        df['percent'] = df['cum_sum'] / df['total_sum']
        df['abc'] = df['percent'].apply(self.abc_segmentation)
        df = df.drop(columns=['cum_sum', 'percent', 'total_sum', 'turnover'])
        return df.squeeze('columns')
