"""soilanalysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_swagger.views import get_swagger_view
from frontend.views import index

schema_view = get_swagger_view(title='Soil Test API', url='/')
urlpatterns = [
    path('api/', include('coredata.urls')),
    path('api/', include('samples.urls')),
    path('api/admin', admin.site.urls),
    url('api/doc', schema_view),
    re_path(r"^$", index),
    re_path(r"^(?:.*)/?$", index),
]
