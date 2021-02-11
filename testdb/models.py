from django.db import models


class DataAssortmentDate(models.Model):
    dt = models.DateField()
    client_id = models.IntegerField()
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'data_assortment_date'


class DataAssortmentInfo(models.Model):
    client_id = models.IntegerField()
    product_cid = models.CharField(max_length=255)
    shop_cid = models.CharField(max_length=255)
    assortment_type = models.ForeignKey('DataAssortmentType', models.DO_NOTHING)
    product = models.ForeignKey('DataProduct', models.DO_NOTHING)
    shop = models.ForeignKey('DataShop', models.DO_NOTHING)
    dt = models.DateField()
    active = models.BooleanField(blank=True, null=True)
    changed = models.BooleanField()
    assortment_type_cid = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    system_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'data_assortment_info'


class DataAssortmentInfoAssortmentDt(models.Model):
    assortmentinfo = models.ForeignKey(DataAssortmentInfo, models.DO_NOTHING)
    assortmentdate = models.ForeignKey(DataAssortmentDate, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'data_assortment_info_assortment_dt'
        unique_together = (('assortmentinfo', 'assortmentdate'),)


class DataAssortmentType(models.Model):
    cid = models.CharField(max_length=255)
    active = models.BooleanField()
    client_id = models.IntegerField()
    name = models.CharField(max_length=256)
    changed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'data_assortment_type'
        unique_together = (('cid', 'client_id'),)


class DataAttribute(models.Model):
    cid = models.CharField(unique=True, max_length=100)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'data_attribute'


class DataBrand(models.Model):
    cid = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    update_date = models.DateTimeField()
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    changed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'data_brand'
        unique_together = (('client', 'cid'),)


class DataCategory(models.Model):
    cid = models.CharField(max_length=100)
    parent_cid = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255)
    update_date = models.DateTimeField()
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    changed = models.BooleanField()
    l = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_category'
        unique_together = (('client', 'cid'),)


class DataDataloadlog(models.Model):
    task_id = models.CharField(max_length=150)
    task_type = models.CharField(max_length=150)
    event_type = models.CharField(max_length=150)
    date = models.DateTimeField()
    message = models.TextField()  # This field type is a guess.
    status = models.CharField(max_length=50)
    meta = models.TextField(blank=True, null=True)  # This field type is a guess.
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    event_id = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'data_dataloadlog'


class DataMarker(models.Model):
    cid = models.CharField(max_length=100)
    parent_cid = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    l = models.IntegerField(blank=True, null=True)
    r = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    client_id = models.IntegerField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_marker'
        unique_together = (('client_id', 'cid'),)


class DataMarkerproducts(models.Model):
    client_id = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey('DataProduct', models.DO_NOTHING, blank=True, null=True)
    marker = models.ForeignKey(DataMarker, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_markerproducts'


class DataProduct(models.Model):
    cid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    update_date = models.DateTimeField()
    brand = models.ForeignKey(DataBrand, models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(DataCategory, models.DO_NOTHING, blank=True, null=True)
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    article = models.CharField(max_length=100, blank=True, null=True)
    barcode = models.TextField(blank=True, null=True)
    depth = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    height = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    photo = models.CharField(max_length=100, blank=True, null=True)
    width = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    changed = models.BooleanField()
    sync = models.BooleanField()
    create_dt = models.DateField(blank=True, null=True)
    is_weight = models.BooleanField()
    compression = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    compression_height = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    compression_width = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    compression_depth = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_product'
        unique_together = (('client', 'cid'),)


class DataProductAttribute(models.Model):
    value = models.CharField(max_length=500)
    value_type = models.CharField(max_length=255)
    attribute = models.ForeignKey(DataAttribute, models.DO_NOTHING)
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    product = models.ForeignKey(DataProduct, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'data_product_attribute'
        unique_together = (('client', 'product', 'attribute'),)


class DataProductImage(models.Model):
    photo = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    product = models.ForeignKey(DataProduct, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'data_product_image'
        unique_together = (('client', 'product', 'type'),)


class DataProductInventory(models.Model):
    dt = models.DateField()
    qty = models.DecimalField(max_digits=20, decimal_places=4)
    original_price = models.DecimalField(max_digits=20, decimal_places=4)
    stock_total_price = models.DecimalField(max_digits=20, decimal_places=4)
    changed = models.BooleanField()
    update_date = models.DateTimeField()
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    product = models.ForeignKey(DataProduct, models.DO_NOTHING)
    shop = models.ForeignKey('DataShop', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'data_product_inventory'
        unique_together = (('client', 'shop', 'product', 'dt'),)


class DataProductMessage(models.Model):
    client_id = models.IntegerField()
    product = models.ForeignKey(DataProduct, models.DO_NOTHING)
    user_id = models.IntegerField(blank=True, null=True)
    conf = models.TextField(blank=True, null=True)  # This field type is a guess.
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'data_product_message'


class DataProductPack(models.Model):
    name = models.CharField(max_length=100)
    qty = models.DecimalField(max_digits=14, decimal_places=4)
    height = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True)
    depth = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True)
    width = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True)
    compression = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    product = models.ForeignKey(DataProduct, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'data_product_pack'
        unique_together = (('client', 'product', 'name', 'qty'),)


class DataProductsale(models.Model):
    receipt_id = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField()
    original_price = models.DecimalField(max_digits=20, decimal_places=4)
    price = models.DecimalField(max_digits=20, decimal_places=4)
    qty = models.DecimalField(max_digits=20, decimal_places=4)
    discount = models.DecimalField(max_digits=20, decimal_places=4)
    margin_price_total = models.DecimalField(max_digits=20, decimal_places=4)
    total_price = models.DecimalField(max_digits=20, decimal_places=4)
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    product = models.ForeignKey(DataProduct, models.DO_NOTHING)
    shop = models.ForeignKey('DataShop', models.DO_NOTHING, blank=True, null=True)
    terminal = models.ForeignKey('DataTerminal', models.DO_NOTHING)
    week_day = models.IntegerField(blank=True, null=True)
    dt = models.DateField(blank=True, null=True)
    refund = models.BooleanField(blank=True, null=True)
    bulk = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_productsale'


class DataPromotion(models.Model):
    cid = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)
    date_from = models.DateField()
    date_to = models.DateField()
    changed = models.BooleanField()
    update_date = models.DateTimeField()
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'data_promotion'
        unique_together = (('client', 'cid'),)


class DataPromotionAccess(models.Model):
    changed = models.BooleanField()
    update_date = models.DateTimeField()
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    product = models.ForeignKey(DataProduct, models.DO_NOTHING)
    promotion = models.ForeignKey(DataPromotion, models.DO_NOTHING)
    shop = models.ForeignKey('DataShop', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'data_promotion_access'
        unique_together = (('client', 'promotion', 'shop', 'product'),)


class DataPurchaseProduct(models.Model):
    cid = models.CharField(max_length=100)
    document_id = models.CharField(max_length=100)
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    shop = models.ForeignKey('DataShop', models.DO_NOTHING)
    supplier = models.ForeignKey('DataSupplier', models.DO_NOTHING)
    product = models.ForeignKey(DataProduct, models.DO_NOTHING)
    order_date = models.DateTimeField()
    receive_date = models.DateTimeField()
    price = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    qty = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    price_total = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    changed = models.BooleanField()
    update_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'data_purchase_product'
        unique_together = (('client', 'cid'),)


class DataReceiveProduct(models.Model):
    cid = models.CharField(max_length=100)
    document_id = models.CharField(max_length=100)
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    shop = models.ForeignKey('DataShop', models.DO_NOTHING)
    supplier = models.ForeignKey('DataSupplier', models.DO_NOTHING)
    product = models.ForeignKey(DataProduct, models.DO_NOTHING)
    document_date = models.DateTimeField()
    price = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    qty = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    price_total = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    changed = models.BooleanField()
    update_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'data_receive_product'
        unique_together = (('client', 'cid'),)


class DataShop(models.Model):
    cid = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    update_date = models.DateTimeField()
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    changed = models.BooleanField()
    format = models.ForeignKey('DataShopformat', models.DO_NOTHING, blank=True, null=True)
    group_id = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_shop'
        unique_together = (('client', 'cid'),)


class DataShopAccess(models.Model):
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    shop = models.ForeignKey(DataShop, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'data_shop_access'
        unique_together = (('client', 'shop', 'user'),)


class DataShopGroups(models.Model):
    group_id = models.CharField(primary_key=True, max_length=-1)
    parent_id = models.CharField(max_length=-1, blank=True, null=True)
    name = models.CharField(max_length=-1, blank=True, null=True)
    client_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'data_shop_groups'
        unique_together = (('client_id', 'group_id'),)


class DataShopformat(models.Model):
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    cid = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    changed = models.BooleanField()
    update_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'data_shopformat'
        unique_together = (('client', 'cid'),)


class DataSupplier(models.Model):
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    cid = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    changed = models.BooleanField()
    update_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'data_supplier'
        unique_together = (('client', 'cid'),)


class DataTerminal(models.Model):
    cid = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    update_date = models.DateTimeField()
    client = models.ForeignKey('ProfileClient', models.DO_NOTHING)
    shop = models.ForeignKey(DataShop, models.DO_NOTHING)
    changed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'data_terminal'
        unique_together = (('client', 'shop', 'cid'),)
