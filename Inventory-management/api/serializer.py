from rest_framework import serializers
from base.models import Products,Category,Supplier

class CategorySerializer(serializers.Serializer):
    id=serializers.IntegerField(write_only=True)
    name=serializers.CharField(read_only=True)

class SupplierSerializer(serializers.Serializer):
   id=serializers.IntegerField(write_only=True)
   name=serializers.CharField(read_only=True)


class ProductSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField()
    
    category_id=serializers.IntegerField(write_only=True)
    supplier_id=serializers.ListField(write_only=True)
    category=CategorySerializer(read_only=True)
    supplier=SupplierSerializer(read_only=True,many=True)
    price=serializers.FloatField()
    quantity=serializers.FloatField()
    created_at=serializers.DateTimeField(read_only=True)
    updated_at=serializers.DateTimeField(read_only=True)
    
#temporary

class ProductCategorySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    category_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    ) 
