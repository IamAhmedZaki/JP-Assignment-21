from django.db import models

class Category(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    
#class Supplier(models.Model):
#    id=models.AutoField(primary_key=True)
#    name=models.CharField(max_length=200)


class Products(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category')
    #supplier_id=models.ManyToManyField(Supplier,related_name='supplier')
    price=models.FloatField()
    quantity=models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)