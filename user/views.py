from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import UserModel, Customer
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

class UserHomeView(View):
    def get(self, request):
        return render(request, 'user/home.html')


class UserLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('customer-list')
    


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    

    
class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'user/customer-list.html'
    context_object_name = 'customers'

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'user/customer-create.html'
    fields = ['name', 'email', 'phone', 'address']
    success_url = reverse_lazy('customer-list')

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'user/customer-update.html'
    fields = ['name', 'email', 'phone', 'address']
    context_object_name = 'customer'
    success_url = reverse_lazy('customer-list')

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'user/customer-delete.html'
    context_object_name = 'customer'
    success_url = reverse_lazy('customer-list')

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
@require_POST
@login_required
def get_customers(request):
    print('request', request)
    print("customer")
    if is_ajax(request) and request.method == 'POST':
        term = request.POST.get('term', '')
        # Search by code instead of name
        customers = Customer.objects.filter(
            code__icontains=term
        ).values('id', 'code', 'name')
        
        customer_list = list(customers)
        return JsonResponse(customer_list, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)