# from django.db import models
from rest_framework import status
import secrets
from .models import *
from datetime import datetime
from .models import Token
from rest_framework import permissions
# from .models import UserRole, RolePermission, User


def generate_custom_model_token(custom_model_id):
    try:
        custom_model_instance = User.objects.get(user_id=custom_model_id)
        token = secrets.token_hex(20)
        Token.objects.create(user=custom_model_instance, key=token, created=datetime.now())
        return token
    except User.DoesNotExist:
        return None, {'error': 'Custom model not found'}, status.HTTP_404_NOT_FOUND


class TokenPermissionView(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            authorization_header = request.META.get('HTTP_AUTHORIZATION', '')

            if authorization_header.startswith('Token '):
                token = authorization_header[len('Token '):]
                token_obj = Token.objects.get(key=token)
                user = token_obj.user_id
                user_role = Userrole.objects.get(user=user)
                role = user_role.r_id
                perm = UserRolePermission.objects.filter(r=role).values('p_id')
                for i in range(len(perm)):
                    if 7 == perm[i]['p_id']:
                        return True
        except (Token.DoesNotExist, Userrole.DoesNotExist, UserRolePermission.DoesNotExist):
            return False


class TokenPermissionPost(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            authorization_header = request.META.get('HTTP_AUTHORIZATION', '')

            if authorization_header.startswith('Token '):
                token = authorization_header[len('Token '):]
                token_obj = Token.objects.get(key=token)
                user = token_obj.user_id
                user_role = Userrole.objects.get(user=user)
                role = user_role.r_id
                perm = UserRolePermission.objects.filter(r=role).values('p_id')
                for i in range(len(perm)):
                    if 5 == perm[i]['p_id']:
                        return True
        except (Token.DoesNotExist, Userrole.DoesNotExist, UserRolePermission.DoesNotExist):
            return False


class TokenPermissionPut(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            authorization_header = request.META.get('HTTP_AUTHORIZATION', '')

            if authorization_header.startswith('Token '):
                token = authorization_header[len('Token '):]
                token_obj = Token.objects.get(key=token)
                user = token_obj.user_id
                user_role = Userrole.objects.get(user=user)
                role = user_role.r_id
                perm = UserRolePermission.objects.filter(r=role).values('p_id')
                for i in range(len(perm)):
                    if 6 == perm[i]['p_id']:
                        return True
        except (Token.DoesNotExist, Userrole.DoesNotExist, UserRolePermission.DoesNotExist):
            return False


class TokenPermissionDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            authorization_header = request.META.get('HTTP_AUTHORIZATION', '')

            if authorization_header.startswith('Token '):
                token = authorization_header[len('Token '):]
                token_obj = Token.objects.get(key=token)
                user = token_obj.user_id
                user_role = Userrole.objects.get(user=user)
                role = user_role.r_id
                perm = UserRolePermission.objects.filter(r=role).values('p_id')
                for i in range(len(perm)):
                    if 8 == perm[i]['p_id']:
                        return True
        except (Token.DoesNotExist, Userrole.DoesNotExist, UserRolePermission.DoesNotExist):
            return False