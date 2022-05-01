from django.urls import path

from samples import views


urlpatterns = [
    path('contraclist',views.Contract_filter.as_view()),
    path('agreemant',views.Agrement.as_view()),
    path('createuser',views.UserListAPIView.as_view()),
    path('user/<int:id>',views.UserUpdate.as_view(),name='home'),
    path('userchangepassword/<int:id>',views.ChangePasswordUserView.as_view()),
    path('samples', views.SampleListCreate.as_view()),
    path('samples/<pk>', views.SampleDetailsUpdateDelete.as_view()),
    path('excel/samples', views.SampleExcel.as_view()),
    path('statistics/samples', views.SampleStatistics.as_view()),
]
