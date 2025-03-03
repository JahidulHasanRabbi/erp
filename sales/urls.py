from django.urls import path
from .views import  ProductUpdateView, ProductDeleteView, ProductDetailView, ProductCreateView, ProductListView, SalesCreate, SalesDeleteView, SalesDetailView, SalesListView, get_items_ajax_view

urlpatterns = [
    


    path('product/', ProductListView.as_view(), name='product-list'),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/<str:code>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<str:code>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<str:code>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    
    # Sales URLs
    path('list/', SalesListView.as_view(), name='sales-list'),
    path('new-sales/', SalesCreate, name='sales-create'),
    path('<int:pk>/', SalesDetailView.as_view(), name='sales-detail'),
    path('<int:pk>/delete/', SalesDeleteView.as_view(), name='sales-delete'),

]