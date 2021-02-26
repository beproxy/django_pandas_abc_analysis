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
            qs = DataProductsale.objects.filter(total_price__gte=0).values('receipt_id', 'total_price', "shop__name")[:100000]
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        df.total_price = pd.to_numeric(df["total_price"])
        df = df.groupby(["shop__name", 'receipt_id']).total_price.sum()
        df = df.to_frame()
        df = df.groupby("shop__name").total_price.mean()
        df = df.to_frame()
        df = df.rename(columns={'total_price': "average_receipt_id"})
        return df

    # Turnover of brands
    def turnover_brands(self):
        try:
            qs = DataProductsale.objects.filter(total_price__gte=0).values("shop__name", 'total_price', 'product__brand__name')[:100000]
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        df = df.groupby(['product__brand__name']).total_price.sum()
        df = df.to_frame()
        df = df.rename(columns={'total_price': "turnover_brands"})
        return df

    # Quantity of sales by brands
    def quantity_sales_brands(self):
        try:
            qs = DataProductsale.objects.filter(qty__gte=0).values('qty', "product__brand__name")
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        df.groupby(['product__brand__name']).qty.sum()
        df = df.to_frame()
        df = df.rename(columns={'qty': "sales_quantity"})
        return df.to_json()

    # Quantity of receipts by brands
    def quantity_receipts_brands(self):
        try:
            qs = DataProductsale.objects.filter(total_price__gte=0).values('receipt_id', "product__brand__name")
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        df = df.groupby(['product__brand__name']).size()
        df = df.to_frame()
        df = df.rename(columns={'receipt_id': "receipt_quantity"})
        return df.to_json()

    def aggregate_data_brands(self):
        try:
            qs = DataProductsale.objects.filter(total_price__gte=0).values(
                "shop__cid", 'product__brand__cid', 'receipt_id', 'qty', 'total_price')[:100000]
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        df = df.groupby(["shop__cid", 'product__brand__cid', 'receipt_id']).sum().reset_index()
        df = df.groupby(['shop__cid', 'product__brand__cid']).agg({
            'receipt_id': 'count',
            'qty': 'sum',
            'total_price': 'sum'}).reset_index()
        df = df.rename(columns={'total_price': "turnover", 'qty': "sales_quantity", 'receipt_id': "receipt_quantity"})
        df = (df.groupby(['shop__cid', 'product__brand__cid'])[['receipt_quantity', 'sales_quantity', 'turnover']]
              .apply(lambda x: x.to_dict())
              .reset_index(name='data')
              .groupby('shop__cid')[['product__brand__cid', 'data']]
              .apply(lambda x: x.set_index('product__brand__cid')['data'].to_dict())
              )
        return df.to_json()

    # ABC analysis of products by turnover by the shop ID
    def abc_analysis(self, id):
        try:
            qs = DataProductsale.objects.filter(shop_id=id, total_price__gte=0).values('total_price', "product__cid")
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        df = df.groupby(['product__cid']).total_price.sum()
        df = df.to_frame()
        df = df.rename(columns={'total_price': "turnover"})
        df = df.sort_values(by='turnover', ascending=False)
        df['cum_sum'] = df['turnover'].cumsum()
        df['total_sum'] = df['turnover'].sum()
        df['percent'] = df['cum_sum'] / df['total_sum']
        df['abc'] = df['percent'].apply(self.abc_segmentation)
        df = df.drop(columns=['cum_sum', 'percent', 'total_sum', 'turnover'])
        return df.to_json()

    # ABC analysis of products by turnover by all shops
    def shops_abc_analysis(self):
        try:
            qs = DataProductsale.objects.filter(total_price__gte=0).values('shop__cid', 'total_price', "product__cid")[:100000]
        except Exception as err:
            print(err)
        df = pd.DataFrame(qs)
        df.set_index(['shop__cid', 'product__cid'], inplace=True)
        df = df.groupby(['shop__cid', 'product__cid']).total_price.sum()
        df = df.to_frame()
        df = df.rename(columns={'total_price': "turnover"})
        df = df.sort_values(by=['shop__cid', 'turnover'], ascending=False)
        df['cum_sum'] = df['turnover'].cumsum()
        df['total_sum'] = df['turnover'].sum()
        df['percent'] = df['cum_sum'] / df['total_sum']
        df['abc'] = df['percent'].apply(self.abc_segmentation)
        df = df.drop(columns=['cum_sum', 'percent', 'total_sum', 'turnover'])
        df.reset_index(inplace=True)
        print(df.head(50))
        df = (df.groupby(['shop__cid', 'product__cid'])[['abc']]
              .apply(lambda x: x.to_dict())
              .reset_index(name='data')
              .groupby('shop__cid')[['product__cid', 'data']]
              .apply(lambda x: x.set_index('product__cid')['data'].to_dict())
              )
        return df.to_json()
