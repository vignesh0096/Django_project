from django.urls import path
from .views import *

urlpatterns = [
    path('permissiongenerator/', PermissionGenerator.as_view()),
    path('rolecreation/', RoleCreation.as_view()),
    path('usercreation/', UserCreation.as_view()),
    path('login/', Login.as_view()),
    path('product_creation/', CreateProduct.as_view()),
    path('view_products/', ViewProducts.as_view()),
    path('change_product/', ChangeProduct.as_view()),
    path('delete_product/', RemoveProduct.as_view()),
]