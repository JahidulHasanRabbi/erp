from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from simpleerp import settings
from .views import (
    CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView, UserLoginView, UserLogoutView, get_customers,
)


urlpatterns = [
    path('accounts/login/', UserLoginView.as_view(), name='login'),
     path('accounts/logout/', UserLogoutView.as_view(), name='logout'),

    path('customer/', CustomerListView.as_view(), name='customer-list'),
    path('customer/create/', CustomerCreateView.as_view(), name='customer-create'),
    path('customer/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer-update'),
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete'),

    path('get_customers/', get_customers, name='get-customers'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)