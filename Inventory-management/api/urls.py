from django.urls import path
from . import views

urlpatterns=[
    path('products/',views.product_get_post),
    path('products/<id>/',views.product_get_delete_put),
    path('categories/',views.category_get_post),
    path('categories/<id>/',views.category_get_delete_put),
    #path('suppliers/',views.supplier_get_post),
    #path('suppliers/<id>/',views.supplier_get_delete_put),
]