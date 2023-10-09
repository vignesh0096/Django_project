from django.db import models


class UserManager(models.Manager):
    def create(self, email, password, name, phone_no,roles):
        user = self.models(email=email, password=password,name=name,phone_no=phone_no,role = roles)
        user.save(using=self._db)


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    email = models.CharField(unique=True, max_length=100)
    objects = UserManager

    class Meta:
        managed = False
        db_table = 'user'


class RolesManager(models.Manager):
    def create(self, role):
        role_name=self.models(role='r_name')
        role_name.save(using=self._db)


class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role = models.CharField(db_column='Role', max_length=100)  # Field name made lowercase.
    objects = RolesManager

    class Meta:
        managed = False
        db_table = 'roles'


class UserRoleManager(models.Manager):
    def add(self,user_id,role_id):
        user = self.models(u_id=user_id,r_id=role_id)
        user.save(using=self._db)


class Userrole(models.Model):
    u = models.ForeignKey('User', models.DO_NOTHING)
    r = models.ForeignKey('Roles', models.DO_NOTHING)
    objects = UserRoleManager

    class Meta:
        managed = False
        db_table = 'userrole'


class PermissionManager(models.Manager):
    def create(self,name, codename, model_name, app_name):
        permission = self.models(name= 'name',codename = 'codename', model_name='model_name', app_name= 'app_name')
        permission.save(using=self._db)


class Permission(models.Model):
    perm_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    app_name = models.CharField(max_length=100, blank=True, null=True)
    objects = PermissionManager

    class Meta:
        managed = False
        db_table = 'permission'


class UserRolePermissionManager(models.Manager):
    def add(self, role_id, perm_id):
        userRole = self.models(role_id=role_id, permission_id=perm_id)
        userRole.save(using=self._db)


class UserRolePermission(models.Model):
    role = models.ForeignKey('Roles', models.DO_NOTHING)
    permission = models.ForeignKey('Permission', models.DO_NOTHING)
    objects = UserRolePermissionManager

    class Meta:
        managed = False
        db_table = 'user_role_permission'


class Permissiongenerator(models.Model):
    model_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'permissiongenerator'


class TokenManager(models.Manager):
    pass


class Token(models.Model):
    key = models.CharField(max_length=100)
    created = models.DateTimeField()
    user = models.ForeignKey('User', models.DO_NOTHING)
    objects = TokenManager

    class Meta:
        managed = False
        db_table = 'Token'


class ProductManager(models.Manager):
    pass


class Products(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.IntegerField()
    objects = ProductManager

    class Meta:
        managed = False
        db_table = 'Products'
