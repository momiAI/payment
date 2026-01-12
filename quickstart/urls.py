from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'quickstart' 

urlpatterns = [
    path('items/',views.all_items,name='items_list'),
    path('register/', views.register_views, name = 'register_user'),
    path('login/', views.login_views, name = 'login_user'),
    path('item/add/', views.add_item_to_cart, name = 'item_add'),
    path('cart/',views.cart_view, name = 'cart_view'),
    path('cart/remove/<int:item_id>/', views.remove_item_from_cart, name='remove_from_cart')
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)