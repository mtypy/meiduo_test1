from django.contrib import admin

# Register your models here.
from goods import models
from goods.models import Goods

admin.site.register(Goods)

admin.site.register(models.GoodsCategory)
admin.site.register(models.GoodsChannel)

admin.site.register(models.Brand)
admin.site.register(models.GoodsSpecification)
admin.site.register(models.SpecificationOption)
admin.site.register(models.SKU)
admin.site.register(models.SKUSpecification)
admin.site.register(models.SKUImage)