# from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import hashers
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from django.apps import apps
from django.contrib.auth.hashers import check_password
from .Token import *
from drf_yasg.utils import swagger_auto_schema


class PermissionGenerator(CreateAPIView):
    serializer_class = PermissionGeneratorCustomSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = PermissionGeneratorSerializer(data=request.data)
        if serializer_class.is_valid():
            model = apps.get_models()
            for model in model:
                if model.__name__ == request.data['model_name']:
                    serializer_class.save()
                    Permission.objects.create(name= 'create_' + str(serializer_class.data['model_name']) + '_permission' ,
                                              codename = 'create_' + str(serializer_class.data['model_name']),
                                              model_name=str(serializer_class.data['model_name']), app_name='new_project_app')
                    Permission.objects.create(name='edit_' + str(serializer_class.data['model_name']) + '_permission',
                                              codename='edit_' + str(serializer_class.data['model_name']),
                                              model_name=str(serializer_class.data['model_name']),
                                              app_name='new_project_app')
                    Permission.objects.create(name='view_' + str(serializer_class.data['model_name']) + '_permission',
                                              codename='view_' + str(serializer_class.data['model_name']),
                                              model_name=str(serializer_class.data['model_name']),
                                              app_name='new_project_app')
                    Permission.objects.create(name='delete_' + str(serializer_class.data['model_name']) + '_permission',
                                              codename='delete_' + str(serializer_class.data['model_name']),
                                              model_name=str(serializer_class.data['model_name']),
                                              app_name='new_project_app')
                    return Response({'response_code': status.HTTP_200_OK,
                                     'message': "Permission Created",
                                     'status_flag': True,
                                     'status': "success",
                                     'error_details': None,
                                     'data': serializer_class.data})

            return Response({'response_code' : status.HTTP_400_BAD_REQUEST,
                             'message' : 'Enter valid credentials',
                             'status' : 'Failed'})


class RoleCreation(CreateAPIView):
    serializer_class = RoleSerializerCustom

    def post(self, request, *args, **kwargs):
        serializer_class = RoleSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            add = Permission.objects.get(codename='create_Products').perm_id
            edit = Permission.objects.get(codename='edit_Products').perm_id
            view = Permission.objects.get(codename='view_Products').perm_id
            delete = Permission.objects.get(codename='delete_Products').perm_id
            role_id = serializer_class.data['role_id']
            if serializer_class.data['role'] == 'ADMIN':
                UserRolePermission.objects.create(role_id=role_id, permission_id=add)
                UserRolePermission.objects.create(role_id=role_id, permission_id=edit)
                UserRolePermission.objects.create(role_id=role_id, permission_id=view)
                UserRolePermission.objects.create(role_id=role_id, permission_id=delete)
            elif serializer_class.data['role'] == 'TL':
                UserRolePermission.objects.create(role_id=role_id,permission_id=add)
                UserRolePermission.objects.create(role_id=role_id, permission_id=edit)
                UserRolePermission.objects.create(role_id=role_id, permission_id=view)
            elif serializer_class.data['role'] == 'USER':
                UserRolePermission.objects.create(role_id=role_id, permission_id=view)

            return Response({'data': 'Roles added successfully'})
        return Response({'response': 'Failed'})


class UserCreation(CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.filter(email=request.data['email'])
            if user:
                return Response('You are already a user')
            else:
                password = hashers.make_password(request.data['password'])
                data = User.objects.create(email=request.data['email'], password=password,
                                           phone_number=request.data['phone_number'], name=request.data['name'])
                serializer_class = CustomUserSerializer(data=request.data)
                if serializer_class.is_valid():
                    if serializer_class.data['role'] == 'ADMIN':
                        user_id = data.user_id
                        role_id = Roles.objects.get(role=serializer_class.data['role']).role_id
                        user_role=Userrole.objects.create(u_id=user_id,r_id= role_id)
                    elif serializer_class.data['role'] == 'TL':
                        user_id = data.user_id
                        role_id = Roles.objects.get(role=serializer_class.data['role']).role_id
                        user_role=Userrole.objects.create(u_id=user_id, r_id=role_id)
                    elif serializer_class.data['role'] == 'USER':
                        user_id = data.user_id
                        role_id = Roles.objects.get(role=serializer_class.data['role']).role_id
                        user_role=Userrole.objects.create(u_id=user_id, r_id=role_id)
                return Response({'response_code': status.HTTP_200_OK,
                                 'message': "signed in succesfully",
                                 'status_flag': True,
                                 'status': "success",
                                 'error_details': None,
                                 'data': serializer_class.data})

        except Exception as error:
            return Response({'response_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': "cant register",
                             'status_flag': False,
                             'status': "Failed",
                             'error_details': str(error),
                             'data': []})


class Login(CreateAPIView):
    """This Api is used for Token creation and Login """
    serializer_class = LoginCustomSerializer

    def post(self, request, *args, **kwargs):
        try:
            mail = User.objects.get(email=request.data['email'])
            password_check = check_password(request.data['password'], mail.password)
            if password_check:
                data = User.objects.filter(email=request.data['email'])
                serializer = LoginSerializer(data, many=True)
                token = generate_custom_model_token(mail.user_id)

                data_response = {
                    'response_code': status.HTTP_200_OK,
                    'message': "logged in succesfully",
                    'status_flag':True,
                    'status': "success",
                    'error_details': None,
                    'data':{'user':serializer.data},
                    }
                return Response(data_response)
            else:
                data_response = {
                    'response_code': status.HTTP_400_BAD_REQUEST,
                    'message': "email not registered",
                    'status_flag': False,
                    'status': "success",
                    'error_details': None,
                    'data': []}
                return Response(data_response)
        except Exception as error:
            return Response({
                'response_code':status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message':'INTERNAL_SERVER_ERROR',
                'status_flag': False,
                'status': "success",
                'error_details': str(error),
                'data': []})


class CreateProduct(CreateAPIView):
    serializer_class = ProductCustomSerializer
    permission_classes = [TokenPermissionPost]

    def post(self, request, *args, **kwargs):
        try:
            serializer_class = ProductSerializer(data=request.data)
            if serializer_class.is_valid(raise_exception=True):
                value = serializer_class.save()
                data_response = {
                    'response_code': status.HTTP_200_OK,
                    'message': "Product Created succesfully",
                    'status_flag': True,
                    'status': "success",
                    'method': request.method,
                    'error_details': None,
                    'data': {'user': serializer_class.data}}
                return Response(data_response)
            else:
                data_response = {
                    'response_code': status.HTTP_400_BAD_REQUEST,
                    'message': "email not registered",
                    'status_flag': False,
                    'status': "Failed",
                    'error_details': None,
                    'data': []}
                return Response(data_response)
        except Exception as error:
            return Response({
                'response_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'INTERNAL_SERVER_ERROR',
                'status_flag': False,
                'status': "Failed",
                'error_details': str(error),
                'data': []})


class ViewProducts(RetrieveAPIView):
    permission_classes = [TokenPermissionView]
    queryset = Products.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = Products.objects.all()
        serializer_class = ProductSerializer(queryset, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "message": "success",
            "data": serializer_class.data,
            "request": request.method,
        }
        return Response(response, status=status.HTTP_200_OK)


class ChangeProduct(UpdateAPIView):

    serializer_class = ProductCustomSerializer
    permission_classes = [TokenPermissionPut]
    queryset = Products.objects.all()

    def put(self, request, *args, **kwargs):
        changes = Products.objects.get(id=request.data['id'])
        serializer_class = ProductSerializer(instance=changes, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            data = {
                'response': 'success',
                'data': [serializer_class.data]
            }
            return Response(data)
        return Response(serializer_class.errors)


class RemoveProduct(DestroyAPIView):
    serializer_class = DeleteProductSerializer
    permission_classes = [TokenPermissionDelete]
    queryset = Products.objects.all()

    @swagger_auto_schema(request_body=serializer_class)
    def delete(self, request, *args, **kwargs):
        query = Products.objects.filter(id=request.data['id'])
        query.delete()
        response = {
            "status": status.HTTP_200_OK,
            "message": "successfully deleted",
        }
        return Response(response, status=status.HTTP_200_OK)