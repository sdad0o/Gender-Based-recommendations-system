from django.db import models
from django.contrib.auth.models import User
# Create your models here.
CATEGORY=(
    ('FBO','F_books'), 
    ('FAC','F_accessory'),
    ('FSC','F_skinCare'),
    ('FBP','F_beauty_products'),
      
    ('MAC','M_accessory'),
    ('MBO','M_books'),
    ('MTO','M_Tool'),
    ('MFT','M_fitness'),
)
class Product (models.Model):
    title = models.CharField( max_length=100)
    description = models.TextField()
    price =models.FloatField()
    category = models.CharField(choices =CATEGORY, max_length=3)
    product_imge =models.ImageField( upload_to='Product')
    product_url = models.URLField(blank=True)
    def __str__(self):
        return self.title 
    
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Wishlist of {self.user.username}"

class Contact(models.Model):
    name =models.CharField(max_length=100)
    email=models.EmailField()
    phone_number=models.CharField(max_length=20)
    message=models.TextField()
    def __str__(self):
        return self.name        