# from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import hashers
from rest_framework.generics import CreateAPIView, GenericAPIView, DestroyAPIView, RetrieveAPIView
from django.apps import apps


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
            add = Permission.objects.get(codename='create_User').perm_id
            edit = Permission.objects.get(codename='edit_User').perm_id
            view = Permission.objects.get(codename='view_User').perm_id
            delete = Permission.objects.get(codename='delete_User').perm_id
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
            user = User.objects.filter(email= request.data['email'])
            if user:
                return Response('You are already a user')
            else:
                password = hashers.make_password(request.data['password'])
                data = User.objects.create(email = request.data['email'], password=password,
                                            phone_number = request.data['phone_number'], name = request.data['name'])
                serializer_class = UserSerializer(data=request.data)
                if serializer_class.is_valid():
                    if serializer_class.data['role'] == 'ADMIN':
                        user_id = data.user_id
                        role_id = Roles.objects.get(serializer_class.data['role']).role_id
                        user = Userroles.objects.create(user_id,role_id)
                    elif serializer_class.data['role'] == 'TL':
                        user_id = data.user_id
                        role_id = Roles.objects.get(serializer_class.data['role']).role_id
                        user = Userroles.objects.create(user_id,role_id)
                    elif serializer_class.data['role'] == 'USER':
                        user_id = data.user_id
                        role_id = Roles.objects.create(serializer_class.data['role']).role_id
                        user = Userroles.objects.add(user_id,role_id)

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
