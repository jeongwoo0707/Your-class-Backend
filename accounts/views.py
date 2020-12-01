import traceback

from django.contrib.auth import get_user_model
# 이메일 전송 관련 Imports
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
# Rest Framework
from rest_framework import (generics, permissions, status, )
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenViewBase

from .email.token import account_activation_token
from .models import CustomUser, Profile
from .serializers import (CustomUserSerializer, ProfileSerializer,
                          ProfileAvatarSerializer,
                          CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer)


class UserRegisterApiView(generics.CreateAPIView):
    """ 새로운 사용자를 생성한다. """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def create(self, request, *args, **kwargs):
        """ 에러 발생 시, 해당 항목을 출력하도록 변경 """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserManageApiView(generics.RetrieveUpdateAPIView):
    """ 인증된 사용자를 관리한다. """
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    # 일반적으로 APIView 클래스의 queryset 속성에 모델을 연결해 사용하지만,
    # 오직 로그인된 사용자의 모델만 가져오기 위해서 GenericAPIView 클래스의 get_object 메소드를 오버라이드한다.
    def get_object(self):
        """ 인증된 사용자를 가져와 반환한다. """
        # 'authentication_classes' 속성 때문에, request 오브젝트에 user 속성이 존재한다.
        return self.request.user


class CustomTokenObtainPairView(TokenViewBase):
    """ 토큰 획득 시 토큰의 만료시간을 JSON에 추가하기 위한 View """
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenViewBase):
    """ 토큰 재발급 시 토큰의 만료시간을 JSON에 추가하기 위한 View """
    serializer_class = CustomTokenRefreshSerializer


class UserActivateApiView(APIView):
    """ 이메일 인증을 위해 전송한 URL 정보를 통해 접근하는 View """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, uidb64, token):
        """ 오직 HTTP GET 방식만 처리하며, 유저를 활성화(Activation)한다. """
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))  # Base64 디코딩
            user = get_user_model().objects.get(pk=uid)      # 유저 정보를 가져온다.
        except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        try:
            # 유저가 존재하며, 이메일에 제공된 토큰과 동일한 토큰을 가지고 있는 경우
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True   # 유저 활성화
                user.save()             # 변경 내용 DB 저장
                return Response(user.email + '계정이 활성화 되었습니다', status=status.HTTP_200_OK)
            else:
                return Response('만료된 링크입니다', status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print(traceback.format_exc())


class ProfileListApiView(generics.ListAPIView):
    """ 사용자 프로필 목록을 출력한다. """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]


class ProfileManageApiView(generics.RetrieveUpdateAPIView):
    """ 사용자 프로필 세부내용을 확인한다. (유저 세부 정보 전부 표현) """
    # queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        """ 인증된 사용자의 프로필을 가져와 반환한다. """
        # 'authentication_classes' 속성 때문에, request 오브젝트에 user 속성이 존재한다.
        return self.request.user.profile


class AvatarManageApiView(generics.UpdateAPIView):
    """ 사용자 프로필의 아바타를 수정한다. (삭제불가) """
    serializer_class = ProfileAvatarSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        """ 인증된 사용자의 프로필을 가져와 반환한다. """
        # 'authentication_classes' 속성 때문에, request 오브젝트에 user 속성이 존재한다.
        return self.request.user.profile
