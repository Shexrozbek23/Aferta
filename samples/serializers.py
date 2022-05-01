from rest_framework import serializers
from .models import Sample,Oferta,inspection_general,type_service,product_type


class SampleSerializer(serializers.ModelSerializer):
    name_calculation_region = serializers.ReadOnlyField(source='calculation_region_name')
    name_creator = serializers.ReadOnlyField(source='creator_name')
    name_crop_type = serializers.ReadOnlyField(source='crop_type_name')
    class Meta:
        model = Sample
        fields = '__all__'
        extra_fields = ('name_calculation_region', 'name_creator', 'name_crop_type')
        read_only_fields = ('adder_district', 'creator')


class inspection_generalSerializer(serializers.ModelSerializer):
    class Meta:
        model =inspection_general
        fields = "__all__"


class type_serviceSerializer(serializers.ModelSerializer):
    class Meta:
        model =type_service
        fields = "__all__"


class product_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model =product_type
        fields = "__all__"


class reemantSerializer(serializers.ModelSerializer):
    product_type=product_typeSerializer()
    service_type=type_serviceSerializer()
    general_inspection=inspection_generalSerializer()
    class Meta:
        model =Oferta
        fields = "__all__"


class AgreemantSerializer(serializers.ModelSerializer):
    class Meta:
        model =Oferta
        fields = ['region','payment_amount','district','cadastre_number','product_type','square_of_services','applicant_organization','applicant_tin','applicant_fullname','applicant_phone','service_type']
        extra_kwargs = {
            'region': {'required': True},
            'district': {'required': True},
            'service_type':{'required': True},
            'cadastre_number': {'required': True},
            'product_type': {'required': False},
            'square_of_services': {'required': True},
            'applicant_organization':{'required': True},
            'applicant_tin': {'required': True},
            'applicant_fullname': {'required': True},
            'applicant_phone': {'required': True},
            'payment_amount': {'required': False}
        }

        
class ShSerializer(serializers.ModelSerializer):
     class Meta:
        model =Oferta
        fields = ['applicant_tin','code_number']