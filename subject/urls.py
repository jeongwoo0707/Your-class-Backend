from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('enroll', views.EnrollViewSet)
# enroll : Request를 보낸 user가 수강 중인 과목 조회
app_name = "subject"
urlpatterns = [
    # create : subject 생성 (POST)
    path('create', views.CreateSubjectApiView.as_view(), name='create'),
    # subjectenroll : 과목을 수강중인 학생 조회 subjectenroll?Id=<subjectId> (GET)
    path('subjectenroll',views.SubjectEnrollView.as_view(), name = 'subenroll'),
    # detail : 과목 정보 조회, 과목 정보 수정, 과목 삭제 detail/<subjectId> (GET,PUT,DELETE)
    # PUT 은 "subjectTimeList" : "화요일 1교시, 목요일 2교시" 로 보낼것 
    path('detail/<int:pk>/',views.SubjectView.as_view(), name = 'subjectDetail'),
    # reset : invitationCode 재설정 reset/<subjectId> (PUT)
    # PUT null 하면 invitationCode 재설정함
    path('reset/<int:pk>/',views.ResetInvitationView.as_view(), name='reset'),
    # invite : invitationCode 에 해당하는 과목 조회 invite/<invitationCode> (GET)
    path('invite/<invitationCode>/',views.InviteView.as_view(), name='invite'),
    # invite/enroll : 현재 user와 invitationcode에 해당하는 과목 연결 invite/enroll/<invitationCode> (POST)
    path('invite/enroll/<invitationCode>/',views.EnrollView.as_view(), name = 'inviteEnroll'),
    # invite/enroll : 현재 수강생을 삭제한다. invite/enroll/<subjectId>/<userId> (DELETE)
    path('enroll/delete/<int:subjectId>/<int:userId>/',views.EnrollView.as_view(), name = 'deleteEnroll'),
    path('', include(router.urls)),
]