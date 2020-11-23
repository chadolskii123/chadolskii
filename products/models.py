import os
import random

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse

from ecomm.utils import unique_slug_generator


# 확장자 확인
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(filepath)
    return name, ext


# 랜덤 파일 이름 설정
def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    print(new_filename)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(fitured=True)

    def search(self, query):
        lookups = Q(title__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query) \
                  | Q(tag__title__icontains=query)
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def featured(self):
        return self.get_queryset().featured()

    # def featured(self):  # Product.objects.featured()
    #     return self.get_queryset().featured()

    def all(self):
        return self.get_queryset().all()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)  # Product.objects
        if qs.count() == 1:
            return qs.first()
        return None

    def active(self):
        return self.get_queryset().active()

    def search(self, query):
        return self.get_queryset().search(query)


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, default='', unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    # FileField는 다 들어가짐, ImageField는 이미지 파일만 들어와짐
    image = models.ImageField(upload_to=upload_image_path, null=True,
                              blank=True)  # 앞에는 / 없고 뒤에 넣어야 함 - setting에 설정한 media root 로 갈 듯
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_digital = models.BooleanField(default=False)


    objects = ProductManager()

    def get_absolute_url(self):
        # return "/products/{slug}".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def get_downloads(self):
        # qs = self.productfile_set.all()
        qs = self.productfile_set.all()
        return qs


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


def upload_product_file_loc(instance, filename):
    slug = instance.product.slug
    if slug:
        location = "product/{}".format(slug)
    else:
        slug = unique_slug_generator(instance.product)
        location = "product/{}".format(slug)
    return location + filename  # /path/to/filename.mp4


class ProductFile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_product_file_loc,
                            storage=FileSystemStorage(location=settings.PROTECTED_ROOT)
                            )

    def __str__(self):
        return str(self.file.name)

    def get_download_url(self):
        return self.file.url

    @property
    def name(self):
        return self.file.name
