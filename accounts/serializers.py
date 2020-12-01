from datetime import datetime

from django.contrib.auth import get_user_model
from django.conf import settings
# 이메일 전송 관련 Imports
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
# Rest Framework Serializers
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from .email.token import account_activation_token
from .email import text
from .models import Profile


class CustomUserSerializer(serializers.ModelSerializer):
    """ 커스텀 유저 모델을 직렬화(Serialize)한다. """
    # 기존 Model 필드를 덮어씌워 새롭게 정의한다.
    password = serializers.CharField(write_only=True,
                                     min_length=8,
                                     style={'input_type': 'password'})
    # Password 확인을 위해 새로운 필드를 하나 생성한다.
    password_confirm = serializers.CharField(write_only=True,
                                             style={'input_type': 'password'})
    # 프로필 모델을 문자열 형태로 받아온다.
    # profile = serializers.StringRelatedField()

    class Meta:
        model = get_user_model()
        # Serializing 과정에서 'Validate'할 필드의 목록...이들은 'validated_data'가 된다.
        fields = ('id', 'email', 'name', 'birthday','school', 'password', 'password_confirm', 'is_student')
        read_only_fields = ('id', )

    # 완전한 객체 인스턴스를 생성할 때 호출되는 create 메소드를 오버라이드한다.
    def create(self, validated_data):
        """ 새로운 유저를 생성하고 반환한다. (serializer.is_valid() 호출 시 실행된다) """
        # CustomUserManager 클래스에 정의한 create_user 메소드를 호출하여 비밀번호를 암호화하고 CustomUser 생성.
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            birthday=validated_data['birthday'],
            school=validated_data['school'],
            password=validated_data['password'],
            is_student=validated_data['is_student'],
            # password_confirm 필드는 필요하지 않으므로, **validated_data 사용하지 않는다.
        )

        user.is_active = False  # 이메일 인증을 하지 않은 경우, is_active 값을 False
        user.save()  # 변경 내용을 DB 저장

        # 인증 토큰과 관련된 변수
        domain = # 본인이 사용할 front end URL 입력
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = account_activation_token.make_token(user)

        # 이메일 전송과 관련된 변수
        mail_subject = '[Your class] 회원가입 인증 메일입니다.'
        mail_content = text.message(domain, uidb64, token)

        to_email = user.email
        email = EmailMessage(mail_subject,  # 이메일 제목
                             mail_content,  # 이메일 내용
                             to=['tom9744@dgu.ac.kr', to_email, ]  # 이메일 수신자
                             )
        email.send()  # 이메일 전송

        return user

    # 'set_password' 메소드가 호출되는 것을 확실히 하기위해, update 메소드도 오버라이드한다.
    def update(self, instance, validated_data):
        """ 비밀번호를 set_password 메소드를 통해 설정하고 유저 정보를 업데이트 및 반환한다. """
        password = validated_data.pop('password', None)  # validated_data 딕셔너리에서 password 필드를 제거한다.
        user = super().update(instance, validated_data)  # super()를 통해 ModelSerializer 클래스의 update 메소드 호출.

        if password:
            user.set_password(password)
            user.save()

        return user

    def validate_birthday(self, value):
        """ birthday 필드에 대한 Validation 과정 """
        today = datetime.now().date()
        if (today - value).days < 2555:
            raise serializers.ValidationError("만 7세 이하는 가입할 수 없습니다.")
        return value

    def validate(self, data):
        """ password, password_confirm 필드에 대한 Validation 과정 """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("두 비밀번호가 일치하지 않습니다.")
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ 토큰 획득 시 만료시간을 추가하기 위한 시리얼라이저 """
    def validate(self, attrs):
        data = super().validate(attrs)

        data['access_expiration_date'] = datetime.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        data['refresh_expiration_date'] = datetime.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """ 토큰 재발급 시 만료시간을 추가하기 위한 시리얼라이저 """
    def validate(self, attrs):
        data = super().validate(attrs)

        data['access_expiration_date'] = datetime.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

        return data


class ProfileSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer(read_only=True)
    avatar = serializers.ImageField(read_only=True, use_url=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'nickname', 'avatar', )
        read_only_fields = ('id',)

    def validate_nickname(self, value):
        if len(value) > 20:
            raise serializers.ValidationError('닉네임은 20글자를 넘을 수 없습니다.')
        return value


class ProfileAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('nickname', 'avatar',)
        read_only_fields = ('nickname', )
