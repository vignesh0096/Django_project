from django.urls import path
from .views import *

urlpatterns = [
    path('permissiongenerator/', PermissionGenerator.as_view()),
    path('rolecreation/', RoleCreation.as_view()),
    path('usercreation/', UserCreation.as_view()),
]