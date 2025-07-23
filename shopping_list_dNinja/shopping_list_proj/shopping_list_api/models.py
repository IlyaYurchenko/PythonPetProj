from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    is_purchased = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} {self.quantity}'
    
    class Meta:
        ordering = ['name']
    