import random
from django.db import models
from django.forms import model_to_dict
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

from user.models import Customer

# Proudct

class Product(models.Model):
    code = models.CharField(max_length=6, unique=True)
    slug = AutoSlugField(unique=True, populate_from='name')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    vendor = models.CharField(max_length=255)
    catagory = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product-list", kwargs={"code": self.code})
    
    def save(self, *args, **kwargs):
        if not self.code: 
            self.code = self.generate_unique_product_code()
        super().save(*args, **kwargs)


    @staticmethod
    def generate_unique_product_code():
        while True:
            code = random.randint(100000, 999999) 
            if not Customer.objects.filter(code=code).exists():
                return code
    
    def to_json(self):
        print('model_to_dict(self)', model_to_dict(self))
        product = model_to_dict(self)
        product['code'] = self.code
        product['text'] = self.name
        product['stock'] = self.stock
        product['price'] = self.price
        product['vendor'] = self.vendor
        product['catagory'] = self.catagory
        return product
        

    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'





#sales

class SalesModel(models.Model):
    
    sales_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    grandtotal = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return (
            f'{self.id} - {self.sales_date.strftime("%d-%m-%Y")} - {self.grandtotal}'
        )

    class Meta:
        db_table = 'sales'
        verbose_name = 'Sales'
        verbose_name_plural = 'Sales'


class SalesDetailsModel(models.Model):
    sales = models.ForeignKey(SalesModel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.id} - {self.sales} - {self.product}'
    

    class Meta:
        db_table = 'sales_details'
        verbose_name = 'Sales Detail'
        verbose_name_plural = 'Sales Details'

