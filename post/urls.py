from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

app_name = "post"
urlpatterns = [
    # 공지사항을 등록함 
    # createNotice (POST)
    # classId 보내야함! (POST)
    path('createNotice', views.CreateNoticeApiView.as_view(), name='createNotice'),
    # 질문을 등록함
    # createQuestion (POST)
    # classId 보내야함! (POST)
    path('createQuestion', views.CreateQuestionApiView.as_view(), name ='createQuestion'),
    # subjectId 에 해당하는 모든 공지사항+ 질문 출력
    # postList/<subjectId> (GET)
    path('postList/<int:subjectId>', views.PostApiListView.as_view(), name='postList'),
    # subjectId 에 해당하는 모든 공지사항 출력
    # NoticeList/<subjectId> (GET)
    path('noticeList/<int:subjectId>', views.NoticeApiListView.as_view(), name='noticeList'),
    # subjectId 에 해당하는 모든 질문 출력
    # QuestionList/<subjectId> (GET)
    path('questionList/<int:subjectId>', views.QuestionApiListView.as_view(), name = 'questionList'),
    # postId 에 해당하는 글 출력, 수정, 삭제
    # postDetail/<postId> (GET, PUT, DELETE)
    path('postDetail/<int:postId>', views.PostApiDetailView.as_view(), name= 'postDetail'),
    # 댓글을 등록함
    # createComment (POST)
    # postId 보내야함!
    path('createComment', views.CreateCommentApiView.as_view(), name='createComment'),
    # postId에 해당하는 모든 댓글 출력
    # commentList/<postId> (GET)
    path('commentList/<int:postId>', views.CommentApiListView.as_view(), name='commentList'),
    # commentId 에 해당하는 댓글 수정, 삭제
    # commentDetail/<commentId> (PUT, DELETE)
    path('commentDetail/<commentId>',views.CommentDetailView.as_view(), name='commentDetail'),
]