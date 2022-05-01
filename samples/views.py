
from django.conf import settings
from django.shortcuts import render
from rest_framework import generics, views, response, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.http import Http404
from .cumma import calculation
from django.db.models import Sum
import datetime
from django.views import View
from django.template.loader import render_to_string
from coredata.models import User,Reference
from coredata.serializers import (
    ReferenceSerializer,
    AllUserSerializer,
    CreateUserSerializer,
    UserPasswordChangeSerializer,
    UserSerializer,
    ReferenceCreateSerializer,
    UserCreateSerializer,
    ChangeCreateSerializer
)
from coredata.permissions import PaidServicePermission
from coredata.models import District,User
from .models import Oferta, Sample,type_service,inspection_general,Oferta_detail
from .serializers import SampleSerializer,AgreemantSerializer,reemantSerializer,ShSerializer
from django.http import HttpResponse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa 


import xlwt


from io import BytesIO,StringIO

class Contract_filter(views.APIView):
    def get(self,request):
        inn=self.request.query_params.get("inn")
        code_nomer=self.request.query_params.get("code_nomer")
        contract=Oferta.objects.filter()
        if inn !=None:
            contract=contract.filter(applicant_tin=inn)
        if code_nomer !=None:
            contract=get_object_or_404(Oferta,code_number=code_nomer)
            template_path = 'newfile.html'
            if contract.service_type.id<=5:
                contract.service_type.type='Qishloq xo\'jaligiga mo\'ljallangan yerlarning agrokimyoviy tahlili'
                numer_or_hectare='Gektar'
            else:
                numer_or_hectare='Namuna'
            print(contract.service_type.type)
            oferta_detail=get_object_or_404(Oferta_detail,id=1)
            info={
                    "id": contract.id,
                    "product_type": {
                        "id": contract.product_type.id,
                        "type": contract.product_type.type,
                        
                    },
                    "service_type": {
                        "id": contract.service_type.id,
                        "type": contract.service_type.type,
                        "value": contract.service_type.value,
                       
                    },
                    "general_inspection": {
                        "id": contract.general_inspection.id,
                        "name": contract.general_inspection.name,
                        
                    },
                    "code_number": contract.code_number,
                    "given_date":  contract.given_date,
                    "cadastre_number": contract.cadastre_number,
                    "square_of_services": contract.square_of_services,
                    "payment_amount": contract.payment_amount,
                    "paid_amount": contract.paid_amount,
                    "applicant_organization": contract.applicant_organization,
                    "applicant_tin": contract.applicant_tin,
                    "applicant_fullname": contract.applicant_fullname,
                    "applicant_phone": contract.applicant_phone,
                    "added_at": "2022-04-29T06:15:54.124708Z",
                    "updated_at": "2022-04-29T06:15:54.641506Z",
                    "region": contract.region.name_en,
                    "district": contract.district.name_en,
                    'numer_or_hectare':numer_or_hectare,
                    'adress':oferta_detail.adress,
                    'x_r':oferta_detail.x_r,
                    'sh_x':oferta_detail.sh_x,
                    'bank':oferta_detail.bank,
                    'mfo':oferta_detail.mfo,
                    'oked':oferta_detail.oked,
                    'inn':oferta_detail.inn,
                    'phone_number':oferta_detail.phone_number
                }
            print(info)
            
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(info)

            # create a pdf
            pisa_status = pisa.CreatePDF(
            html.encode('UTF-8'), dest=response)
            # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        return Response(ShSerializer(contract,many=True).data,status=status.HTTP_200_OK)

class Agrement(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        all_agreemant=Oferta.objects.all()
        serializer=AgreemantSerializer(all_agreemant,many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer=AgreemantSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            regionall=District.objects.filter(region__id=serializer.data.get('region'))
            #Check there is district in region
            if not regionall.filter(id=serializer.data.get('district')).exists():
                return Response({"error":"district is existent"},status=status.HTTP_400_BAD_REQUEST)
            if type_service.objects.filter(id=serializer.data.get('service_type')).exists():
                type=type_service.objects.get(id=serializer.data.get('service_type'))
                if serializer.data.get('square_of_services')>0 :
                    print(type_service.value,serializer.data.get('square_of_services'))
                    count=serializer.data.get('square_of_services')*type.value
                else:
                    return Response({"error":"servece_type is is existent ", "success": False},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"You entered minuse number ", "success": False},status=status.HTTP_400_BAD_REQUEST)
            data['payment_amount']=count
            type=type_service.objects.get(id=serializer.data.get('service_type'))
            current_year = int(datetime.datetime.now().strftime('%y'))
            if int(serializer.data.get('region')) < 10:
                first_four_digits = str(current_year) + '0' + str(serializer.data.get('region'))
            else:
                first_four_digits = str(current_year) + str(serializer.data.get('region'))
            if int(type.id) < 10:
                first_six_digits = str(first_four_digits) + '0' + str(type.id)
            else:
                first_six_digits = str(first_four_digits) + str(type.id)
            last_invoice = Oferta.objects.filter(code_number__startswith=first_six_digits).order_by(
                                'code_number').last()
            if last_invoice:
                invoice_number = int(last_invoice.code_number) + 1
            else:
                invoice_number = int(first_six_digits) * 100000 + 1
            rector=inspection_general.objects.get(id=1)
            data['general_inspection']=rector
            data['code_number']=invoice_number
            oneagremment = Oferta.objects.create(**data)
            oneagremment.save()
            
            return Response(reemantSerializer(oneagremment).data)
        else:
            return Response(serializer.errors)


# Get Alluser here
class Alluser(generics.ListAPIView):
    serializer_class = AllUserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

# Create all user here
class UserListAPIView(views.APIView):
    def get(self, request):
        # getting only own collectors
        users = User.objects.filter(region=request.user.region)
        return response.Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        user = User.objects.filter(region=request.user.region, status_code=True).exclude(pk=request.user.pk)
        testregion=User.objects.filter(region=request.user.region,status_code=True)
        testdistrict=District.objects.filter(region=request.user.region).values('id')
        # chack thera is district in District model 
        
        if request.user.user_role==2:
            return response.Response(
                        {"error": 'You can not create new user '},
                    status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid() and request.user.status_code:
            data = serializer.validated_data
            district = data.get('district')

            if testdistrict.filter(id=district.id).exists():
                pass
            else:
                return response.Response(
                        {"error": 'This district is not avalible.'},
                    status=status.HTTP_400_BAD_REQUEST)
            if request.user.user_role == 1 and district.region != request.user.region:
                return response.Response({"error": 'District not found'}, status=status.HTTP_400_BAD_REQUEST)
            for i in testregion:
                if i.district.id==district.id:
                    return response.Response(
                        {"error": 'This district is currently have collector.'},
                        status=status.HTTP_400_BAD_REQUEST)
            
            password = data.pop('password')
            user = User.objects.create(**data)
                      
            
            if request.user.user_role == 1:
                user.user_role = 2
                user.region = request.user.region
            if password is not None:
                user.set_password(password)
            user.save()
            return response.Response(UserCreateSerializer(user).data, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            



class UserUpdate(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        user = get_object_or_404(User,status_code=True, pk=id)
        print(user,request.user.user_role,user.user_role,request.user.region,user.region)
        if request.user.user_role == 0 or request.user.user_role == 1 or (request.user.region == user.region and request.user.district==user.district):

            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, id):
        testregion=User.objects.filter(region=request.user.region,status_code=True)
        user = get_object_or_404(User,status_code=True, id=id)
        
        serializer=ChangeCreateSerializer(user,data=request.data)
        if request.user==user:
            return response.Response({"error": "You can not edit."},
                                     status=status.HTTP_400_BAD_REQUEST)
       
        if serializer.is_valid():
            if request.data.get('district')!=None:
                districttest=get_object_or_404(District,id=request.data.get('district'))
                print(districttest.region,request.user.region,request.user.user_role)
                if districttest.region!=request.user.region and request.user.user_role==1:
                    return response.Response({"error": 'District not avalible'}, status=status.HTTP_400_BAD_REQUEST)
                for i in testregion:
                        if i.district.id==districttest.id:
                            return response.Response(
                                {"error": 'This district is currently have collector.'},
                                status=status.HTTP_400_BAD_REQUEST)
            if request.user.user_role==1 and user.user_role==2 and request.user.region==user.region :
               
                user.user_role = 2
                user.region = request.user.region
                serializer.save()
                return response.Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            else:
                return response.Response({"error":"You can not edit this user"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        users = get_object_or_404(User,status_code=True, id=id)
        if request.user.user_role==1 and request.user.status_code and users.region==request.user.region:
        
            users.delete()  
            return Response(status=status.HTTP_204_NO_CONTENT) 
        elif request.user.user_role==0:
            users.delete()  
            return Response({"userdelete":"User Not found"},status=status.HTTP_204_NO_CONTENT) 
        else:
            return Response({"error":"You con't delete this user"},status=status.HTTP_400_BAD_REQUEST)
#Change password of user here
class ChangePasswordUserView(views.APIView):
    permission_classes = [IsAuthenticated, PaidServicePermission]
    
    def get(self, request,id):
        user=User.objects.get(id=id)
        serializer = UserSerializer(user)
        return response.Response(serializer.data)
    
    def post(self, request,id):
        user = get_object_or_404(User,status_code=True, pk=id)
        serializer = UserPasswordChangeSerializer(data=request.data)
        user_info_serializer = UserSerializer(user)
        if serializer.is_valid():
            if (request.user==user) or (request.user.user_role==1 and request.user.region==user.region) or request.user.user_role==0: 

                old_password = serializer.data.get("old_password")
                if not user.check_password(old_password):
                    return response.Response(
                        {
                            "old_password": ["Wrong password."]
                        },
                        status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                user.set_password(serializer.data.get("new_password"))
                user.save()
                return response.Response(user_info_serializer.data, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateReference(views.APIView):
    def get(self,request):
        print(request.user.region,request.user.district)
        queryset=Reference.objects.filter(region_id=request.user.region.id,district_id=request.user.district.id)
        serializer=ReferenceSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializers=ReferenceCreateSerializer(data=request.data)
        if serializers.is_valid():
            print(serializers.data)
            return Response(serializers.data,status=status.status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class ReferenceAPi(generics.ListAPIView):
    serializer_class = ReferenceSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Reference.objects.all()
        region_id= self.request.query_params.get("region_id")
        district_id= self.request.query_params.get("district_id")
        if region_id is not None:
            queryset = queryset.filter(region=region_id)
        if district_id is not None:
            queryset = queryset.filter(distrcit=district_id)
        return queryset

class SampleStatistics(views.APIView):
    permission_classes = (IsAuthenticated, PaidServicePermission,)

    def get(self, request):
        type = request.query_params.get("type")
        calculation_region = request.query_params.get("calculation_region")
        calculation_district = request.query_params.get("calculation_district")
        requested_all = Sample.objects.all()
        user = self.request.user
        if user.region is not None:
            requested_all = Sample.objects.filter(calculation_region=user.region)
        if type is None:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)
        if calculation_region is not None:
            requested_all = Sample.objects.filter(calculation_region__pk=calculation_region)
            if user.region is not None:
                requested_all = Sample.objects.filter(calculation_region=user.region)
                if type == "potassium":
                    lowest_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.lowest,
                                                                 calculation_region=user.region)
                    low_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.low,
                                                              calculation_region=user.region)
                    highest_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.highest,
                                                                  calculation_region=user.region)
                    high_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.high,
                                                               calculation_region=user.region)
                    normal_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.normal,
                                                                 calculation_region=user.region)
                if type == "phosphorus":
                    lowest_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.lowest,
                                                                 calculation_region=user.region)
                    low_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.low,
                                                              calculation_region=user.region)
                    highest_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.highest,
                                                                  calculation_region=user.region)
                    high_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.high,
                                                               calculation_region=user.region)
                    normal_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.normal,
                                                                 calculation_region=user.region)
                if type == "humus":
                    lowest_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.lowest,
                                                                 calculation_region=user.region)
                    low_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.low,
                                                              calculation_region=user.region)
                    highest_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.highest,
                                                                  calculation_region=user.region)
                    high_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.high,
                                                               calculation_region=user.region)
                    normal_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.normal,
                                                                 calculation_region=user.region)
            else:
                if type == "potassium":
                    lowest_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.lowest,
                                                                 calculation_region__pk=calculation_region)
                    low_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.low,
                                                              calculation_region__pk=calculation_region)
                    highest_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.highest,
                                                                  calculation_region__pk=calculation_region)
                    high_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.high,
                                                               calculation_region__pk=calculation_region)
                    normal_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.normal,
                                                                 calculation_region__pk=calculation_region)
                if type == "phosphorus":
                    lowest_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.lowest,
                                                                 calculation_region__pk=calculation_region)
                    low_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.low,
                                                              calculation_region__pk=calculation_region)
                    highest_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.highest,
                                                                  calculation_region__pk=calculation_region)
                    high_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.high,
                                                               calculation_region__pk=calculation_region)
                    normal_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.normal,
                                                                 calculation_region__pk=calculation_region)
                if type == "humus":
                    lowest_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.lowest,
                                                                 calculation_region__pk=calculation_region)
                    low_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.low,
                                                              calculation_region__pk=calculation_region)
                    highest_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.highest,
                                                                  calculation_region__pk=calculation_region)
                    high_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.high,
                                                               calculation_region__pk=calculation_region)
                    normal_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.normal,
                                                                 calculation_region__pk=calculation_region)
        else:
            if user.region is not None:
                if type == "potassium":
                    lowest_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.lowest, calculation_region=user.region)
                    low_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.low, calculation_region=user.region)
                    highest_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.highest, calculation_region=user.region)
                    high_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.high, calculation_region=user.region)
                    normal_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.normal, calculation_region=user.region)
                if type == "phosphorus":
                    lowest_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.lowest, calculation_region=user.region)
                    low_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.low, calculation_region=user.region)
                    highest_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.highest, calculation_region=user.region)
                    high_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.high, calculation_region=user.region)
                    normal_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.normal, calculation_region=user.region)
                if type == "humus":
                    lowest_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.lowest, calculation_region=user.region)
                    low_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.low, calculation_region=user.region)
                    highest_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.highest, calculation_region=user.region)
                    high_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.high, calculation_region=user.region)
                    normal_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.normal, calculation_region=user.region)
            else:
                if type == "potassium":
                    lowest_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.lowest)
                    low_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.low)
                    highest_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.highest)
                    high_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.high)
                    normal_requested_all = Sample.objects.filter(provided_level_potassium=Sample.Status.normal)
                if type == "phosphorus":
                    lowest_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.lowest)
                    low_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.low)
                    highest_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.highest)
                    high_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.high)
                    normal_requested_all = Sample.objects.filter(provided_level_phosphorus=Sample.Status.normal)
                if type == "humus":
                    lowest_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.lowest)
                    low_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.low)
                    highest_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.highest)
                    high_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.high)
                    normal_requested_all = Sample.objects.filter(provided_level_humus=Sample.Status.normal)
        if calculation_district is not None:
            lowest_requested_all = lowest_requested_all.filter(calculation_district__pk=calculation_district)
            low_requested_all = low_requested_all.filter(calculation_district__pk=calculation_district)
            highest_requested_all = highest_requested_all.filter(calculation_district__pk=calculation_district)
            high_requested_all = high_requested_all.filter(calculation_district__pk=calculation_district)
            normal_requested_all = normal_requested_all.filter(calculation_district__pk=calculation_district)

        return response.Response({
            'requested_all': requested_all.aggregate(Sum('area'))['area__sum'],
            'lowest_requested_all': lowest_requested_all.aggregate(Sum('area'))['area__sum'],
            'low_requested_all': low_requested_all.aggregate(Sum('area'))['area__sum'],
            'highest_requested_all': highest_requested_all.aggregate(Sum('area'))['area__sum'],
            'high_requested_all': high_requested_all.aggregate(Sum('area'))['area__sum'],
            'normal_requested_all': normal_requested_all.aggregate(Sum('area'))['area__sum']
        }, status=status.HTTP_200_OK)


class SampleListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, PaidServicePermission,)
    queryset = Sample.objects.all().order_by('-id')
    serializer_class = SampleSerializer
    filter_fields = ('crop_type', 'outline_number', 'calculation_region', 'calculation_district',)

    def get_queryset(self):
        user = self.request.user
        samples = Sample.objects.all().order_by('-id')
        if user.region is not None:
            samples = Sample.objects.filter(calculation_region=user.region).order_by('-id')
        return samples

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class SampleDetailsUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, PaidServicePermission,)
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer


provided_levels = {
    'LOWEST': {
        'color': 'yellow',
        'text': 'Жуда кам'
    },
    'LOW': {
        'color': 'red',
        'text': 'Кам'
    },
    'NORMAL': {
        'color': 'light_blue',
        'text': 'Ўртача'
    },
    'HIGH': {
        'color': 'blue',
        'text': 'Юқори'
    },
    'HIGHEST': {
        'color': 'green',
        'text': 'Жуда юқори'
    }
}


class SampleExcel(views.APIView):
    permission_classes = (IsAuthenticated, PaidServicePermission,)

    def getStatusColor(self, row, col_num):
        style = xlwt.XFStyle()
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        style.borders = borders
        style.font.bold = True
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map[provided_levels[row[col_num]]['color']]
        style.pattern = pattern
        return style

    def get(self, request):
        calculation_region = request.query_params.get("calculation_region")
        crop_type = request.query_params.get("crop_type")
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Tuproq tahlili.xls"'

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        ws = wb.add_sheet('Натижалар')

        # Sheet header, first row
        row_num = 0
        excel_row_num = 0
        columns = ['ID', 'Киритилган сана',
                   'Вилоять', 'Туман',
                   'Контур рақами',
                   'Намуна идентификацион рақами',
                   'Майдони', 'Экин тури',
                   'РН нейтрал (pH =7)', 'NO3  (мг/кг ҳисобида)', 'Коэффициент', 'Таъминланганлик даражаси',
                   'Ҳаракатчан P2O5  (мг/кг ҳисобида)',
                   'Коэффициент', 'Таъминланганлик даражаси', 'Алмашинувчан K20 (мг/кг ҳисобида)',
                   'Коэффициент', 'Таъминланганлик даражаси', 'Гумус % ҳисобида', 'Таъминланганлик даражаси', '',
                   '1 ц - N',
                   '1 ц - P', '1 ц - K',
                   'Жами - N', 'Жами - P', 'Жами - K']
        columns_attributes = ['pk', 'added_at',
                              'calculation_region__name_uz',
                              'calculation_district__name_local',
                              'outline_number',
                              'sample_number',
                              'area',
                              'crop_type__name_uz',
                              'given_phosphorus',
                              'given_nitrogen',
                              'coefficient_nitrogen',
                              'provided_level_nitrogen',
                              'given_phosphorus',
                              'coefficient_phosphorus',
                              'provided_level_phosphorus',
                              'given_potassium',
                              'coefficient_potassium',
                              'provided_level_potassium',
                              'given_humus',
                              'provided_level_humus',
                              'usage_per_centner_nitrogen',
                              'usage_per_centner_phosphorus',
                              'usage_per_centner_potassium']
        header_style = xlwt.XFStyle()
        header_style.font.bold = True
        for col_num in range(len(columns)):
            ws.write(excel_row_num, col_num, columns[col_num], style=header_style)
        if calculation_region:
            rows = Sample.objects.filter(calculation_region__pk=calculation_region).order_by(
                '-added_at', '-calculation_district', '-outline_number').values_list(*columns_attributes)
        elif crop_type:
            rows = Sample.objects.filter(crop_type__pk=crop_type).order_by('-added_at', '-calculation_district',
                                                                           '-outline_number').values_list(
                *columns_attributes
            )
        else:
            rows = Sample.objects.all().order_by('-added_at', '-calculation_district', '-outline_number').values_list(
                *columns_attributes)
        unique_identifier = f"{str(rows[0][1])}{rows[0][3]}{rows[0][4]}"
        usage_per_centner_nitrogen = 0
        usage_per_centner_phosphorus = 0
        usage_per_centner_potassium = 0
        all_usage_per_centner_nitrogen = 0
        all_usage_per_centner_phosphorus = 0
        all_usage_per_centner_potassium = 0
        usage_per_centner_humus = 0
        area = 0

        row_style = xlwt.XFStyle()
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        row_style.borders = borders

        bold_text_row_style = xlwt.XFStyle()
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        bold_text_row_style.borders = borders
        bold_text_row_style.font.bold = True
        for row in rows:
            row_num += 1
            excel_row_num += 1
            if unique_identifier != f"{str(row[1])}{row[3]}{row[4]}":
                unique_identifier = f"{str(row[1])}{row[3]}{row[4]}"
                ws.write(excel_row_num, 6, area, bold_text_row_style)
                ws.write(excel_row_num, 21, usage_per_centner_nitrogen, bold_text_row_style)
                ws.write(excel_row_num, 22, usage_per_centner_phosphorus, bold_text_row_style)
                ws.write(excel_row_num, 23, usage_per_centner_potassium, bold_text_row_style)
                ws.write(excel_row_num, 24, all_usage_per_centner_nitrogen, bold_text_row_style)
                ws.write(excel_row_num, 25, all_usage_per_centner_phosphorus, bold_text_row_style)
                ws.write(excel_row_num, 26, all_usage_per_centner_potassium, bold_text_row_style)
                usage_per_centner_nitrogen = row[20]
                usage_per_centner_phosphorus = row[21]
                usage_per_centner_potassium = row[22]
                all_usage_per_centner_nitrogen = row[20] * row[6]
                all_usage_per_centner_phosphorus = row[21] * row[6]
                all_usage_per_centner_potassium = row[22] * row[6]
                area = row[6]
                excel_row_num += 1
                for col_num in range(len(row)):

                    if col_num == 11 or col_num == 14 or col_num == 17 or col_num == 19:
                        try:
                            ws.write(excel_row_num, col_num, provided_levels[row[col_num]]['text'],
                                     self.getStatusColor(row, col_num))
                        except KeyError as e:
                            ws.write(excel_row_num, col_num, "Кўрсатилмаган")
                    elif col_num == 20:
                        ws.write(excel_row_num, col_num + 1, row[col_num], row_style)
                        ws.write(excel_row_num, col_num + 2, row[col_num + 1], row_style)
                        ws.write(excel_row_num, col_num + 3, row[col_num + 2], row_style)
                        ws.write(excel_row_num, col_num + 4, row[20] * row[6], row_style)
                        ws.write(excel_row_num, col_num + 5, row[21] * row[6], row_style)
                        ws.write(excel_row_num, col_num + 6, row[22] * row[6], row_style)
                        break
                    elif col_num == 1:
                        ws.write(excel_row_num, col_num, f"{row[1]}", row_style)
                    else:
                        ws.write(excel_row_num, col_num, row[col_num], row_style)
                # usage_per_centner_humus = 0
            else:

                usage_per_centner_nitrogen += row[20]
                usage_per_centner_phosphorus += row[21]
                usage_per_centner_potassium += row[22]
                all_usage_per_centner_nitrogen += row[20] * row[6]
                all_usage_per_centner_phosphorus += row[21] * row[6]
                all_usage_per_centner_potassium += row[22] * row[6]
                # usage_per_centner_humus += row[20]
                area += row[6]
                for col_num in range(len(row)):
                    if col_num == 11 or col_num == 14 or col_num == 17 or col_num == 19:
                        try:
                            ws.write(excel_row_num, col_num, provided_levels[row[col_num]]['text'],
                                     self.getStatusColor(row, col_num))
                        except KeyError as e:
                            ws.write(excel_row_num, col_num, "Кўрсатилмаган")
                    elif col_num == 20:
                        ws.write(excel_row_num, col_num + 1, row[col_num], row_style)
                        ws.write(excel_row_num, col_num + 2, row[col_num + 1], row_style)
                        ws.write(excel_row_num, col_num + 3, row[col_num + 2], row_style)
                        ws.write(excel_row_num, col_num + 4, row[20] * row[6], row_style)
                        ws.write(excel_row_num, col_num + 5, row[21] * row[6], row_style)
                        ws.write(excel_row_num, col_num + 6, row[22] * row[6], row_style)
                        break
                    elif col_num == 1:
                        ws.write(excel_row_num, col_num, f"{row[1]}", row_style)
                    else:
                        ws.write(excel_row_num, col_num, row[col_num], row_style)
        wb.save(response)
        return response
