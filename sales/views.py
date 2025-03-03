import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.views.decorators.http import require_POST
from user.models import Customer
from .models import Product, SalesModel, SalesDetailsModel
from .form import ProductForm, SalesForm, SalesDetailsFormSet 
from django.contrib.auth.decorators import login_required





# Product Views
class ProductListView(ListView):
    model = Product
    template_name = 'shop/product-list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product-detail.html'
    context_object_name = 'product'
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        code = self.kwargs.get('code')
        return get_object_or_404(queryset, code=code)

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product-create.html'
    success_url = reverse_lazy('product-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Product created successfully!')
        return super().form_valid(form)
    


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product-update.html'
    
    def get_success_url(self):
        return reverse_lazy('product-detail', kwargs={'code': self.object.code})
    
    def form_valid(self, form):
        messages.success(self.request, 'Product updated successfully!')
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        code = self.kwargs.get('code')
        return get_object_or_404(queryset, code=code)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'shop/product-delete.html'
    success_url = reverse_lazy('product-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Product deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        code = self.kwargs.get('code')
        return get_object_or_404(queryset, code=code)


# Sales Views

class SalesListView(ListView):
    model = SalesModel
    template_name = 'shop/sales-list.html'
    context_object_name = 'sales'


class SalesDetailView(DetailView):
    model = SalesModel
    template_name = 'shop/sales-details.html'
    context_object_name = 'sale'

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def SalesCreate(request):
    context = {
        "customer": [C.customer_select() for C in Customer.objects.all()],
    }

    if request.method == 'POST':
        if is_ajax(request):
            try:
                data = json.loads(request.body)

                required_fields = ['customer', 
                                   'subtotal', 
                                   'tax', 
                                   'grandtotal', 
                                   'amount_paid', 
                                   'products']
                
                for field in required_fields:
                    if field not in data:
                        raise ValueError({'error': f'{field} is required'})
                    
                sales = {
                    'customer': Customer.objects.get(pk=data['customer']),
                    'subtotal': data['subtotal'],
                    'tax': data['tax'],
                    'grandtotal': data['grandtotal'],
                    'amount_paid': data['amount_paid'],
                }
                
                with transaction.atomic():
                    sales = SalesModel.objects.create(**sales)

                    product = data['products']
                    if not product:
                        raise ValueError({'error': 'No product found'})
                    
                    for item in product:
                        if not all(
                            key in item for key in ['product', 'quantity', 'price', 'total']
                        ):
                            raise ValueError({'error': 'Invalid product data'})
                        
                        product = Product.objects.get(pk=item['product'])
                        if product.stock < item['quantity']:
                            raise ValueError({'error': 'Product out of stock'})
                        
                        sales_detail = {
                            'sales': sales,
                            'product': product,
                            'quantity': item['quantity'],
                            'price': item['price'],
                            'total': item['total'],
                        }
                        
                        SalesDetailsModel.objects.create(**sales_detail)


                        product.stock -= item['quantity']
                        product.save()

                return JsonResponse({
                    'success': 'Sales created successfully!',
                    'redirect': reverse_lazy('sales-list')})               
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
            except ValueError as e:
                return JsonResponse(e, status=400)
    
    return render(request, 'shop/sales-create.html', context)


class SalesDeleteView(LoginRequiredMixin, DeleteView):
    model = SalesModel
    template_name = 'shop/sales-delete.html'
    success_url = reverse_lazy('sales-list')
    context_object_name = 'sale' 

    
    
@csrf_exempt
@require_POST
@login_required
def get_items_ajax_view(request):
    if is_ajax(request):
        try:
            term = request.POST.get("term", "")
            data = []
            
            if term is None or term.strip() == "":
                items = Product.objects.all()[:30] 
            else:
                items = Product.objects.filter(code__icontains=term)[:30]
                
            for item in items:
                try:
                    item_data = item.to_json()
                    data.append(item_data)
                except Exception as item_error:
                    print(f"Error converting item {item.id} to JSON: {str(item_error)}")
                    continue  
            
            return JsonResponse(data, safe=False)
        except Exception as e:
            print(f"Search error: {str(e)}")  # Log the error
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Not an AJAX request'}, status=400)