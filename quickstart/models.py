from django.db import models
from django.contrib.auth.models import User


class ItemModel(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='items/%Y%m%d', null=True, blank=True)
    description = models.TextField() 
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(ItemModel,related_name='orders')
    created_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def total_value(self):
        return sum(item.price for item in self.items.all())
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
