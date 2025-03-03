from django.contrib import admin
from django.urls import include, path
from sales.views import get_items_ajax_view
from user import urls
from sales import urls
import user


urlpatterns = [
    path('get-products/', get_items_ajax_view, name='get-products'),
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('sales/', include('sales.urls')),
    path('', user.views.UserHomeView.as_view(), name='home'),
    
]
