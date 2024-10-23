from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from base.models import Products,Category,Supplier
from rest_framework import status
from django.db.models import Q,Count,Sum,Avg
from .serializer import CategorySerializer,ProductSerializer,SupplierSerializer,ProductCategorySerializer




@api_view(['GET','POST'])
def category_get_post(request:Request):
    
    if request.method=='GET':
        category=Category.objects.all()
        
        serializer=CategorySerializer(category,many=True)
        return Response(serializer.data,status.HTTP_200_OK)
    
    if request.method=='POST':
        body=request.data
        serializer=CategorySerializer(data=body)
        if serializer.is_valid():
            Category.objects.create(**serializer.validated_data)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        
        data="success"
        
        return Response(data,status.HTTP_201_CREATED)

@api_view(['GET','DELETE','PUT'])
def category_get_delete_put(request:Request,id):
    category=Category.objects.get(pk=id)
    body={}
    if request.method=='GET':
        body={
            'id':category.id,
            'name':category.name
        }
        #serializer=CategorySerializer(body)
        return Response(body,status.HTTP_200_OK)
    if request.method=='PUT':
        data=request.data
        name=data.get('name')
        category.name=name
        category.save()
        data={
            "id":category.id,
            "name":category.name
        }
        data='success'    
        return Response(data,status.HTTP_200_OK)
    
    
    if request.method=='DELETE':
        category.delete()
        data="deleted"
        return Response(data,status.HTTP_200_OK)


@api_view(['GET','POST'])
def supplier_get_post(request:Request):
   if request.method=='GET':
       supplier=Supplier.objects.all()
       serializer=SupplierSerializer(supplier,many=True)
       return Response(serializer.data,status.HTTP_200_OK)
   if request.method=='POST':
       body=request.data
       serializer=SupplierSerializer(data=body)
       if serializer.is_valid():
           Supplier.objects.create(**serializer.validated_data)
       else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
   data='success'
   return Response(data,status.HTTP_201_CREATED) 
       
       
@api_view(['GET','DELETE','PUT'])
def supplier_get_delete_put(request:Request,id):
    supplier=Supplier.objects.get(pk=id)
    if request.method=='GET':
        serializer=SupplierSerializer(supplier)
        return Response(serializer.data,status.HTTP_200_OK)
    
        
    
    if request.method=='PUT':
        serializer=SupplierSerializer(data=request.data)
        if serializer.is_valid():
            for key,value in serializer.validated_data.items():
                setattr(supplier,key,value)
            supplier.save()
            serializer=SupplierSerializer(supplier)
            return Response(serializer.data,status.HTTP_202_ACCEPTED)
        else:
            return Response("invalid data",status.HTTP_400_BAD_REQUEST)
        
    if request.method=='DELETE':
        supplier.delete()
        return Response("Deleted",status.HTTP_200_OK)
    
    return Response("Invalid ID",status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def product_get_post(request:Request):
    data = []
    if request.method == 'GET':
        
        
        name=request.query_params.get('name')
        category_id=request.query_params.get('category_id')
        supplier_id=request.query_params.get("supplier_id")
        
        
        
        
        filters_params={}
        
        if name is not None:
            filters_params["name"]=name
        if category_id is not None:
            filters_params["category_id"]=category_id
        if supplier_id is not None:
            filters_params["supplier__id"]=supplier_id
            
        product= Products.objects.select_related('category').prefetch_related('supplier').filter(**filters_params).distinct()
        
        serializer = ProductSerializer(product, many=True)

        
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            category_id = serializer.validated_data.pop('category_id')
            supplier_id = serializer.validated_data.pop('supplier_id')
            category = Category.objects.filter(id=category_id).first()
            if category is None:
                return Response("invalid category", status=status.HTTP_400_BAD_REQUEST)
            product=Products.objects.create(category=category,**serializer.validated_data)
            supplier=Supplier.objects.filter(id__in=supplier_id)
            product.supplier.add(*supplier)
            
        else:
            return Response( serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    

    
    

    return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

    

@api_view(['GET','DELETE','PUT'])
def product_get_delete_put(request:Request,id):

    products=Products.objects.select_related('category').get(id=id)
    if request.method=='GET':
            
                
        serializer=ProductSerializer(products)
        return Response(serializer.data,status.HTTP_200_OK)
    
    if request.method=='PUT':
        serializer=ProductSerializer(products,data=request.data)
        if serializer.is_valid():
            for key,value in serializer.validated_data.items():
                if key not in ["category_id","supplier"]:
                #product.key=value in a nutshell
                    setattr(products,key,value)
                    
            category_id=serializer.validated_data.pop("category_id")
            if category_id:
                category=Category.objects.get(id=category_id)
                products.category=category
            supplier_id=serializer.validated_data.pop("supplier_id")
            if supplier_id:
                supplier=Supplier.objects.filter(id__in=supplier_id)
                products.supplier.set(supplier)
            
            products.save()
            serializer=ProductSerializer(products)
            
            return Response(serializer.data,status.HTTP_202_ACCEPTED)
            # {
            # "name":"Laptop",
            # "category_id": 2,
            # "supplier_id": [
            #     4,5
            # ],
            # "price":20000,
            # "quantity": 25
            # }


        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)    
        
    if request.method == 'DELETE':
        products.delete()
        data = "deleted"
        return Response(data,status.HTTP_202_ACCEPTED)
    
#temporary
# @api_view(['POST', 'GET'])
# def assign_supplier(requst: Request):
    
#     if requst.method == 'GET':
#         # customers = product_model.objects.select_related("category").all() # will not work due to many-to-many relationship
#         product = Products.objects.prefetch_related("supplier").all()
#         serializer = ProductSerializer(product, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)
        
#     if requst.method=='POST':
#         serializer = ProductCategorySerializer(data=requst.data)
#         if serializer.is_valid():
#             product_id = serializer.validated_data.pop('product_id')
#             cat_ids = serializer.validated_data.pop('category_ids')
            
#             # custom validation
#             # TODO: we could also write this serializer level
#             db_supplier = Supplier.objects.filter(id__in=cat_ids).all()
#             if len(db_supplier) != len(cat_ids):
#                 return Response("One or more category IDs are invalid.", status=status.HTTP_400_BAD_REQUEST)

#             db_product = Products.objects.filter(id=product_id).first()
#             if db_product is None:
#                 return Response("Invalid product.", status=status.HTTP_400_BAD_REQUEST)

            
#             db_product.supplier.set(cat_ids)
#             return Response("success", status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['GET'])
def product_metrics(request:Request):
    category_id=request.query_params.get("category_id")
    product_id=request.query_params.get("product_id")
    products=Products.objects.all()
    
    filter_params={}
    
    if category_id is not None:
        filter_params['category_id']=category_id
    if product_id is not None:
        filter_params['id']=product_id
        
    product=Products.objects.filter(**filter_params).aggregate(total_products=Count('id'),total_stock=Sum('quantity'),average_price=Avg('price'))
    return Response(product,status.HTTP_200_OK)
        
    
@api_view(['GET'])
def category_metrics(request:Request):
    category_id=request.query_params.get("category_id")
    
    filter_params={}
    if category_id is not None:
        filter_params["id"]=category_id
        
    product=Category.objects.filter(**filter_params).aggregate(total_products=Count('category'),stock=Sum('category__quantity'))
    product_stock=product['stock'] or 0
    return Response({"total_product":product['total_products'],"product_stock":product_stock},status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def supplier_metrics(request:Request):
    supplier=request.query_params.get("supplier")
    
    filter_params={}
    if supplier is not None:
        filter_params["name__icontains"]=supplier
    
    total_product=Supplier.objects.prefetch_related('supplier').filter(**filter_params).annotate(total_products=Count('supplier'))
    product=Supplier.objects.prefetch_related('supplier').filter(**filter_params).all()
    highest_count=total_product.order_by('-total_products').first()
    lowest_count=total_product.order_by('total_products').first()
    
    serializer=SupplierSerializer(product,many=True)
    
    return Response({
        "total_product":total_product.aggregate(total=Count("supplier"))['total'],
        "highest_count":highest_count.total_products,
        "lowest_count":lowest_count.total_products,
        "data":serializer.data
    },
                    status.HTTP_200_OK)