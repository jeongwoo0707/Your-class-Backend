from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = "assignment"
urlpatterns = [
    # 과제 생성 
    # classId 보내야함! (POST)
    path('create',views.CreateAssignmentApiView.as_view(), name = 'createAssignment'),
    # 과목 내 과제 리스트 출력 
    # list/<subjectId> (GET)
    path('list/<int:subjectId>',views.AssignmentApiView.as_view(), name= 'assignmentList'),
    # assignmentId 에 해당하는 과제의 상세사항 출력
    # detail/<assignmentId> (GET, DELETE, PUT)
    path('detail/<int:assignmentId>',views.AssignmentDetailView.as_view(), name = 'assignmentDetail'),
    # 과제 세부사항에 존재하는 파일 다운로드
    # download/<assignmentId> (GET)
    path('download/<int:pk>',views.assignment_download_view, name = 'assignmentDownload'),
    # 과제 제출
    # assignId 보내야함! (POST)
    path('submit/create', views.CreateSubmitApiView.as_view(), name = 'createSubmit'),
    # 과제 제출 목록
    # submit/list/<assignmentId> (GET)
    path('submit/list/<int:assignmentId>', views.SubmitApiView.as_view(), name = 'submitList'),
    # 과제 제출 세부사항
    # submit/detail/<submitId> (GET, DELETE, PUT)
    path('submit/detail/<int:assignId>', views.SubmitDetailView.as_view(), name = 'submitDetail'),
    # 과제 제출 파일 다운로드
    # submit/download/<submitId> (GET)
    path('submit/download/<int:pk>', views.submit_download_view, name = 'submitDownload'),
    # 과제 제출 여부 확인
    # isSubmit/<assignmentId> (GET)
    path('isSubmit/<int:assignmentId>', views.IsSubmitView.as_view(), name = 'isSubmit'),
    # 과제 제출 여부 확인(학생 전체)
    # subject/subjectenroll?Id=<subjectId> 로, userId List 받아온 뒤에 해당 userId List를 모두 GET request 받아오면 됩니다!
    # isSubmit/<assignmentId>/<submitUserId> (GET)
    path('isSubmit/<int:assignmentId>/<int:submitUserId>', views.IsSubmitListView.as_view(), name = 'isSubmitList'),
    # 과제 제출 정보(교사 전용)
    # isSubmit/detail/<userId>/<assignmentId> (GET)
    path('isSubmit/detail/<int:userId>/<int:assignmentId>', views.IsSubmitDetailView.as_view(), name='isSubmitDetail')
]
