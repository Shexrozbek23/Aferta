
from wsgiref.validate import validator
from django.db import models
import datetime
from django.core.validators import MaxValueValidator,MinValueValidator 
# Create your models here.
from coredata.models import District, User, Reference, Region
from django.contrib.gis.db import models
from django.contrib.gis.db import models as gis_models

class Sample(models.Model):
    class Status(models.TextChoices):
        low = 'LOW', 'Low'
        lowest = 'LOWEST', 'Lowest'
        normal = 'NORMAL', 'Normal'
        high = 'HIGH', 'High'
        highest = 'HIGHEST', 'Highest'
    namefarm=models.CharField(max_length=250)
    layer=models.FloatField()
    farm_inns=models.IntegerField(validators=[MinValueValidator(100000000),MaxValueValidator(999999999)])
    given_nitrogen = models.DecimalField(max_digits=20, decimal_places=3)
    given_phosphorus = models.DecimalField(max_digits=20, decimal_places=3)
    given_potassium = models.DecimalField(max_digits=20, decimal_places=3)
    given_humus = models.DecimalField(max_digits=20, decimal_places=3)
    provided_level_phosphorus = models.CharField(
        choices=Status.choices,
        max_length=12,
    )
    provided_level_potassium = models.CharField(
        choices=Status.choices,
        max_length=12,
    )
    provided_level_humus = models.CharField(
        choices=Status.choices,
        max_length=12,
    )
    provided_level_nitrogen = models.CharField(
        choices=Status.choices,
        max_length=12,
    )
    coefficient_nitrogen = models.DecimalField(max_digits=20, decimal_places=4)
    coefficient_phosphorus = models.DecimalField(max_digits=20, decimal_places=4)
    coefficient_potassium = models.DecimalField(max_digits=20, decimal_places=4)
    usage_per_centner_nitrogen = models.DecimalField(max_digits=20, decimal_places=4)
    usage_per_centner_phosphorus = models.DecimalField(max_digits=20, decimal_places=4)
    usage_per_centner_potassium = models.DecimalField(max_digits=20, decimal_places=4)
    usage_per_centner_humus = models.DecimalField(max_digits=20, decimal_places=4)
    area = models.DecimalField(max_digits=20, decimal_places=2)
    outline_number = models.TextField(max_length=225, null=True, default='')
    sample_number = models.TextField(max_length=225, null=False,unique=True)
    calculation_region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL,
                                           verbose_name='Calculation Region', related_name='calculation_region')
    calculation_district = models.ForeignKey(District, null=True, on_delete=models.SET_NULL,
                                             verbose_name='Calculation District', related_name='calculation_district')
    crop_type = models.ForeignKey(Reference, null=True, on_delete=models.SET_NULL, verbose_name='Crop Type',
                                  related_name='crop_type')
    added_at = models.DateField(auto_now_add=True, verbose_name='added at', editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name='Creator',
                                related_name='samples')
    field_location = gis_models.MultiPointField(
        "Location in Map", geography=True, blank=True, null=True,
        srid=4326, help_text="Point(longitude latitude)")
    @property
    def calculation_region_name(self):
        if self.calculation_region:
            return self.calculation_region.name_uz
        else:
            return 'None region for this field'

    @property
    def creator_name(self):
        if self.creator:
            return self.creator.username
        else:
            return 'None useer for this field'

    @property
    def crop_type_name(self):
        if self.crop_type:
            return self.crop_type.name_uz
        else:
            return 'None crop for this field'

    class Meta:
        ordering = ['-added_at']
        

class type_service(models.Model):
    type=models.CharField(max_length=500)
    value=models.FloatField()
    added_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Добавлено в')
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    def __str__(self):
        return self.type

class product_type(models.Model):    
    type=models.CharField(max_length=500)
    added_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Добавлено в')
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    def __str__(self):
        return self.type
class inspection_general(models.Model):
    name=models.CharField(max_length=500,default='')
    added_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Добавлено в')
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    def __str__(self):
        return self.name
class Oferta_detail(models.Model):
    adress=models.CharField(max_length=100,verbose_name='Manzil')
    x_r=models.CharField(max_length=90,verbose_name='X/R')
    sh_x=models.CharField(max_length=90,verbose_name='Sh.X')
    bank=models.CharField(max_length=1000,verbose_name='Toshkent shaxar Markaziybank')
    mfo=models.CharField(max_length=50,verbose_name='MFO')
    oked=models.CharField(max_length=500,verbose_name='OKED')
    inn=models.CharField(max_length=15,verbose_name='INN')
    phone_number=models.CharField(max_length=9,verbose_name='Telefon')


    

class Oferta(models.Model):
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, verbose_name='Код региона заявителя')
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING, verbose_name='Код дистрикт заявителя')
    code_number= models.CharField(max_length=18, verbose_name='Номер Оферта', unique=True, null=True,blank=True)
    given_date = models.DateField(auto_now_add=True, verbose_name='Дата выдачи')
    service_type = models.ForeignKey(type_service,on_delete=models.DO_NOTHING,related_name='service_type',verbose_name='Service Type',default=0)
    cadastre_number=models.IntegerField()
    product_type=models.ForeignKey(product_type,on_delete=models.DO_NOTHING,related_name='product_type',verbose_name='product_type',default=0)
    square_of_services = models.FloatField(verbose_name='Количество',default=0)
    payment_amount = models.DecimalField(verbose_name='Сумма платежа', max_digits=15, decimal_places=2,blank=True)
    paid_amount = models.DecimalField(verbose_name='Оплаченное количество', max_digits=15, decimal_places=2,default=0)
    applicant_organization = models.CharField(verbose_name='Организация', max_length=128, null=True)
    applicant_tin = models.CharField(verbose_name='ИНН/ПИНФЛ заявителя', max_length=15, null=True)
    applicant_fullname = models.CharField(verbose_name='ФИО заявителя', max_length=60, null=True)
    applicant_phone = models.CharField(verbose_name='Телефонный номер', max_length=9, null=True)
    general_inspection =  models.ForeignKey(inspection_general, on_delete=models.DO_NOTHING, verbose_name='Директор')
    added_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Добавлено в')
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self):
        return self.applicant_fullname
   