from pickle import FALSE
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.contrib.gis.db import models as gis_models

# Create your models here.


class Country(models.Model):
    code = models.CharField(max_length=100, verbose_name='code')
    name_ru = models.CharField(max_length=250, verbose_name='name_ru')
    name_en = models.CharField(max_length=250)
    name_uz = models.CharField(max_length=250)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name_plural = 'Countries'
        db_table = 'country'


class Region(models.Model):
    name_ru = models.CharField(max_length=512, verbose_name='Название регион')
    name_en = models.CharField(max_length=512, verbose_name='Name of region')
    name_uz = models.CharField(max_length=512, verbose_name='Viloyat nomi', null=True)
    coefficient = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    limit = models.DecimalField(max_digits=20, decimal_places=4, null=True)
    location = gis_models.PointField(
        "Location in Map", geography=True, blank=True, null=True,
        srid=4326, help_text="Point(longitude latitude)")
    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name_plural = 'Regions'
        db_table = 'region'


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, related_name='districts',
                               verbose_name='Область')
    name_ru = models.CharField(max_length=50, verbose_name='Название на русском')
    name_en = models.CharField(max_length=50, verbose_name='Название на английском')
    name_local = models.CharField(max_length=50, verbose_name='Местное название')
    code = models.CharField(max_length=3, unique=True, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    location = gis_models.PointField(
        "Location in Map", geography=True, blank=True, null=True,
        srid=4326, help_text="Point(longitude latitude)")
    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'
        db_table = 'district'


class UserRoles(models.IntegerChoices):
    ADMIN = 0, 'ADMIN'
    WAREHOUSE_MANAGER = 1, 'WAREHOUSE MANAGER'
    COLLECTOR = 2, 'COLLECTOR'


class User(AbstractUser):
    user_role = models.IntegerField(choices=UserRoles.choices, default=UserRoles.COLLECTOR)
    district = models.ForeignKey(District, null=True, on_delete=models.CASCADE, verbose_name='District of point')
    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE, verbose_name='Region of point')
    email = models.EmailField(blank=True)
    status_code=models.BooleanField(default=True,blank=True)
    @property
    def region_name(self):
        if self.region:
            return self.region.name_uz
        else:
            return 'Бу фойдаланувчи учун вилоят белгиланмаган'

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username


class ItemType(models.IntegerChoices):
    POTASSIUM_COEFFICIENT = 1, 'POTASSIUM_COEFFICIENT'
    PHOSPHORUS_COEFFICIENT = 2, 'PHOSPHORUS_COEFFICIENT'
    EXPENSE = 3, 'EXPENSE'
    ANOTHER = 4, 'ANOTHER'


class Reference(models.Model):
    type = models.IntegerField(choices=ItemType.choices, default=ItemType.ANOTHER)
    name_ru = models.CharField(max_length=512, verbose_name='Название', null=True)
    name_en = models.CharField(max_length=512, verbose_name='Name', null=True)
    name_uz = models.CharField(max_length=512, verbose_name='Nomi', null=True)
    status = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)
    val = models.DecimalField(max_digits=30, decimal_places=4, null=True, verbose_name='Qiymati')
    potassium_val = models.DecimalField(max_digits=30, decimal_places=4, default=0, null=True,
                                        verbose_name='Kaliy Qiymati')
    phosphorus_val = models.DecimalField(max_digits=30, decimal_places=4, default=0, null=True,
                                         verbose_name='Fosfor Qiymati')
    nitrogen_val = models.DecimalField(max_digits=30, decimal_places=4, default=0, null=True,
                                       verbose_name='Azot Qiymati')
    code = models.CharField(max_length=512, verbose_name='Kodi', null=True)
    region=models.ForeignKey(Region,on_delete=models.CASCADE,blank=True, null=True)
    district=models.ForeignKey(District,on_delete=models.CASCADE,blank=True, null=True)
    location = gis_models.PointField(
        "Location in Map", geography=True, blank=True, null=True,
        srid=4326, help_text="Point(longitude latitude)")


class SamplesSniffer(models.Model):
    added_at = models.DateTimeField(auto_now_add=True)
    name_uz = models.CharField(max_length=512, verbose_name='Viloyat nomi', null=True)
    limit = models.DecimalField(max_digits=20, decimal_places=4, null=True)

    class Meta:
        db_table = 'samples_sniffer'
