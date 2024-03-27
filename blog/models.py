from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class post(models.Model):
     title=models.CharField(max_length=150)
     desc=models.TextField()
    

class Contact(models.Model):
     sno=models.AutoField(primary_key=True) 
     name=models.CharField(max_length=200)  
     email=models.EmailField(max_length = 254)
     phone=models.CharField(max_length=12)
     desc=models.TextField()
     time=models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.name
