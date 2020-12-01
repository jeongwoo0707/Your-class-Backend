from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

app_name = "schedule"
urlpatterns = [
    # request를 보내는 user가 수강중인 과목 출력 
    # getEnroll (GET)
    path('getEnroll', views.EnrollAPIView.as_view(), name='getEnroll'),
    # subjectId 에 해당하는 모든 과제 출력
    # getAssignment/<subjectId> (GET)
    path('getAssignment/<subjectId>', views.AssignmentAPIView.as_view(), name='getAssignment'),
]