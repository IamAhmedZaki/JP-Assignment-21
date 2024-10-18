from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from base.models import Products,Category#Supplier
from rest_framework import status
from django.db.models import Q
from .serializer import CategorySerializer,ProductSerializer




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


#@api_view(['GET','POST'])
#def supplier_get_post():
#    pass

#@api_view(['GET','DELETE','PUT'])
#def supplier_get_delete_put():
#    pass


@api_view(['GET','POST'])
def product_get_post(request:Request):
    data = []
    if request.method == 'GET':
        
        name=request.query_params.get('name')
        category_id=request.query_params.get('category_id')
        
        
        #product = Products.objects.all()#manual join no query optimizatio
        product = Products.objects.select_related('category').all()#for optimized query
        
        filters=Q()
        
        if name is not None:
            filters &= Q(name__icontains=name)
        if category_id is not None:
            filters &= Q(category_id=category_id)
            
        product= product.filter(filters).all()
        
        serializer = ProductSerializer(product, many=True)

        
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            category_id = serializer.validated_data['category_id']
            category = Category.objects.filter(id=category_id).first()
            if category is None:
                return Response("invalid category", status=status.HTTP_400_BAD_REQUEST)
            product=Products.objects.create(category=category,**serializer.validated_data)
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
                #product.key=value in a nutshell
                setattr(products,key,value)
            products.save()
            serializer=ProductSerializer(products)
            
            return Response(serializer.data,status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)    
        
    if request.method == 'DELETE':
        products.delete()
        data = "deleted"
        return Response(data,status.HTTP_202_ACCEPTED)