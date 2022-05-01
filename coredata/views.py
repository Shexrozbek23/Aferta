# Create your views here.
from django.http import Http404
from requests import Response

from coredata.models import Region, District, Reference, ItemType, User
from coredata.permissions import PaidServicePermission
from coredata.serializers import RegionSerializer, DistrictSerializer, ReferenceSerializer, UserSerializer, \
    UserPasswordChangeSerializer
from rest_framework import mixins, views, generics, viewsets, response, status, permissions



class ReferenceAPi(generics.ListAPIView):
    serializer_class = ReferenceSerializer
    permission_classes = [permissions.IsAuthenticated, PaidServicePermission]
    def get_queryset(self,request):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Reference.objects.all()
        region_id= request.query_params.get("calculation_region")
        district_id= request.query_params.get("calculation_district")
        if region_id is not None:
            queryset = queryset.filter(Reference__region=region_id)
        return queryset


# class ReferenceAPi(views.APIView):
#     permission_classes = [permissions.IsAuthenticated, PaidServicePermission]
    
#     def get(self,request):
#         referenceall=Reference.objects.all()
#         region_id= request.query_params.get("calculation_region")
#         district_id= request.query_params.get("calculation_district")
#         if region_id is not None:
#             referenceall=referenceall.filter(region=region_id)
#         if district_id is not None:
#             referenceall=referenceall.filter(distrcit=district_id)
    


class RegionList(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, PaidServicePermission]
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DistrictList(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, PaidServicePermission]
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    pagination_class = None
    filterset_fields = ['region', ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ExpensetList(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, PaidServicePermission]
    queryset = Reference.objects.filter(type=ItemType.EXPENSE)
    pagination_class = None
    serializer_class = ReferenceSerializer
    filterset_fields = ['code', 'type']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PotassiumCoefficientAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, PaidServicePermission]
    serializer_class = ReferenceSerializer

    def get_object(self, code):
        try:
            return Reference.objects.get(code=code, type=ItemType.POTASSIUM_COEFFICIENT)
        except Reference.DoesNotExist:
            raise Http404

    def get(self, request, code, format=None):
        coefficient = self.get_object(code)
        serializer = self.serializer_class(coefficient)
        return response.Response(serializer.data)


class PhosphorusCoefficientAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, PaidServicePermission]
    serializer_class = ReferenceSerializer

    def get_object(self, code):
        try:
            return Reference.objects.get(code=code, type=ItemType.PHOSPHORUS_COEFFICIENT)
        except Reference.DoesNotExist:
            raise Http404

    def get(self, request, code, format=None):
        coefficient = self.get_object(code)
        serializer = self.serializer_class(coefficient)
        return response.Response(serializer.data)


class ExpenseCoefficientAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, PaidServicePermission]
    serializer_class = ReferenceSerializer

    def get_object(self, pk):
        try:
            return Reference.objects.get(pk=pk)
        except Reference.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        reference = self.get_object(pk)
        serializer = self.serializer_class(reference)
        return response.Response(serializer.data)


class CurrentUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, PaidServicePermission]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return response.Response(serializer.data)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request):
        self.object = self.get_object()
        serializer = UserPasswordChangeSerializer(data=request.data)
        user_info_serializer = UserSerializer(request.user)
        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return response.Response(
                    {
                        "old_password": ["Wrong password."]
                     },
                    status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return response.Response(user_info_serializer.data, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
