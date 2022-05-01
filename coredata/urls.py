from django.urls import path

from coredata import views
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as auth_views

router = DefaultRouter()

urlpatterns = [
    url(r'^auth/$', auth_views.obtain_auth_token),
    url(r'^user/$', views.CurrentUserView.as_view()),
    url(r'^regions/$', views.RegionList.as_view()),
    url(r'^districts/$', views.DistrictList.as_view()),
    url(r'^expenses/$', views.ExpensetList.as_view()),
    url(r'^expenses/(?P<pk>\d+)/$', views.ExpenseCoefficientAPIView.as_view()),
    url(r"^potassium/(?P<code>\d+\.\d+)$", views.PotassiumCoefficientAPIView.as_view()),
    url(r"^phosphorus/(?P<code>\d+\.\d+)$", views.PhosphorusCoefficientAPIView.as_view()),
    # path('', include(router.urls)),
]
