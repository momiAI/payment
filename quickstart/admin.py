from django.contrib import admin
from .models import ItemModel,OrderModel

admin.site.register(ItemModel)
admin.site.register(OrderModel)