# Generated by Django 3.2.8 on 2022-04-28 03:41

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coredata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='agreemant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cadastre_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='inspection_general',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=500)),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено в')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='product_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=500)),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено в')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='type_service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=500)),
                ('value', models.DecimalField(decimal_places=4, max_digits=20)),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено в')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namefarm', models.CharField(max_length=250)),
                ('layer', models.FloatField()),
                ('farm_inns', models.IntegerField(validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(999999999)])),
                ('given_nitrogen', models.DecimalField(decimal_places=3, max_digits=20)),
                ('given_phosphorus', models.DecimalField(decimal_places=3, max_digits=20)),
                ('given_potassium', models.DecimalField(decimal_places=3, max_digits=20)),
                ('given_humus', models.DecimalField(decimal_places=3, max_digits=20)),
                ('provided_level_phosphorus', models.CharField(choices=[('LOW', 'Low'), ('LOWEST', 'Lowest'), ('NORMAL', 'Normal'), ('HIGH', 'High'), ('HIGHEST', 'Highest')], max_length=12)),
                ('provided_level_potassium', models.CharField(choices=[('LOW', 'Low'), ('LOWEST', 'Lowest'), ('NORMAL', 'Normal'), ('HIGH', 'High'), ('HIGHEST', 'Highest')], max_length=12)),
                ('provided_level_humus', models.CharField(choices=[('LOW', 'Low'), ('LOWEST', 'Lowest'), ('NORMAL', 'Normal'), ('HIGH', 'High'), ('HIGHEST', 'Highest')], max_length=12)),
                ('provided_level_nitrogen', models.CharField(choices=[('LOW', 'Low'), ('LOWEST', 'Lowest'), ('NORMAL', 'Normal'), ('HIGH', 'High'), ('HIGHEST', 'Highest')], max_length=12)),
                ('coefficient_nitrogen', models.DecimalField(decimal_places=4, max_digits=20)),
                ('coefficient_phosphorus', models.DecimalField(decimal_places=4, max_digits=20)),
                ('coefficient_potassium', models.DecimalField(decimal_places=4, max_digits=20)),
                ('usage_per_centner_nitrogen', models.DecimalField(decimal_places=4, max_digits=20)),
                ('usage_per_centner_phosphorus', models.DecimalField(decimal_places=4, max_digits=20)),
                ('usage_per_centner_potassium', models.DecimalField(decimal_places=4, max_digits=20)),
                ('usage_per_centner_humus', models.DecimalField(decimal_places=4, max_digits=20)),
                ('area', models.DecimalField(decimal_places=2, max_digits=20)),
                ('outline_number', models.TextField(default='', max_length=225, null=True)),
                ('sample_number', models.TextField(max_length=225, unique=True)),
                ('added_at', models.DateField(auto_now_add=True, verbose_name='added at')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('field_location', django.contrib.gis.db.models.fields.MultiPointField(blank=True, geography=True, help_text='Point(longitude latitude)', null=True, srid=4326, verbose_name='Location in Map')),
                ('calculation_district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='calculation_district', to='coredata.district', verbose_name='Calculation District')),
                ('calculation_region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='calculation_region', to='coredata.region', verbose_name='Calculation Region')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='samples', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('crop_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crop_type', to='coredata.reference', verbose_name='Crop Type')),
            ],
            options={
                'ordering': ['-added_at'],
            },
        ),
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_number', models.CharField(blank=True, max_length=18, null=True, unique=True, verbose_name='Номер Оферта')),
                ('given_date', models.DateField(auto_now_add=True, verbose_name='Дата выдачи')),
                ('cadastre_number', models.IntegerField()),
                ('square_of_services', models.FloatField(default=0, verbose_name='Количество')),
                ('payment_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, verbose_name='Сумма платежа')),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Оплаченное количество')),
                ('applicant_organization', models.CharField(max_length=128, null=True, verbose_name='Организация')),
                ('applicant_tin', models.CharField(max_length=15, null=True, verbose_name='ИНН/ПИНФЛ заявителя')),
                ('applicant_fullname', models.CharField(max_length=60, null=True, verbose_name='ФИО заявителя')),
                ('applicant_phone', models.CharField(max_length=9, null=True, verbose_name='Телефонный номер')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено в')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='coredata.district', verbose_name='Код дистрикт заявителя')),
                ('general_inspection', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='samples.inspection_general', verbose_name='Директор')),
                ('product_type', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_type', to='samples.product_type', verbose_name='product_type')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='coredata.region', verbose_name='Код региона заявителя')),
                ('service_type', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='service_type', to='samples.type_service', verbose_name='Service Type')),
            ],
        ),
    ]