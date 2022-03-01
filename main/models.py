from django.db import models
from django.contrib.auth.models import AbstractUser


# Класс переопределение стандартной модели пользователя для Django
class User(AbstractUser):
    ip = models.GenericIPAddressField(null=False, default='0.0.0.0')
    last_ip = models.GenericIPAddressField(null=False, default='0.0.0.0')
    image = models.ImageField(null=False,
                              default="images/default_avatar/default_avatar.png",
                              upload_to="images/users/")
    is_email_verified = models.BooleanField(null=False, default=False)
    email = models.EmailField(null=False, unique=True)

    first_name = None
    last_name = None


class TypeProduct(models.Model):
    product_type_id = models.AutoField(primary_key=True, null=False)
    product_type_name = models.CharField(max_length=64, null=False, default="Type of product")

    class Meta:
        db_table = 'type_product'


class Product(models.Model):
    product_id = models.AutoField(primary_key=True, null=False)
    product_title = models.CharField(max_length=128, null=False, default="Title of product")
    product_tag = models.CharField(max_length=64, null=False, default="Tag of product")
    product_desc = models.TextField(null=False, default="Description of product")
    product_image = models.ImageField(null=False, upload_to='images/products/', default="images/plug/plug.jpg")
    product_type = models.ForeignKey(TypeProduct, on_delete=models.CASCADE, null=False, default=1)

    class Meta:
        db_table = 'product'


class MiniNews(models.Model):
    mini_news_id = models.AutoField(primary_key=True, null=False)
    mn_title = models.CharField(max_length=128, null=False, default="Title of mini news")
    mn_desc = models.TextField(null=False, default="Description of mini news")
    mn_date = models.DateField(auto_now=True)


class DBManager(models.Manager):
    def __init__(self, using, *args, **kwargs):
        self.db_using = using
        super(DBManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset(using=self.db_using)


class DBModel(models.Model):
    using = 'mdd'

    objects = DBManager(using=using)

    def save(self, *args, **kwargs):
        return super().save(using=self.using, *args, **kwargs)

    def delete(self, *args, **kwargs):
        return super().save(using=self.using, *args, **kwargs)

    class Meta:
        managed = False
        abstract = True
