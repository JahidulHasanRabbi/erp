import random
from django.db import models
from django.contrib.auth.models import User

class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'user_model'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Customer(models.Model):
    code = models.IntegerField(unique=True, editable=False) 
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    address = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code: 
            self.code = self.generate_unique_customer_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_customer_code():
        while True:
            code = random.randint(100000, 999999) 
            if not Customer.objects.filter(customer_code=code).exists():
                return code

    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def customer_select(self):
        return {
            'label': self.name,
            'value': self.code
        }

    class Meta:
        db_table = 'customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'