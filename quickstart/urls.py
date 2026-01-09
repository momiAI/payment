from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'quickstart' 

urlpatterns = [
    path('items/',views.all_items,name='items_list'),
    path('register/', views.register_views, name = 'register_user'),
    path('login/', views.login_views, name = 'login_user')
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)