from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """ 커스텀 유저 모델을 관리하기 위한 클래스 """

    def create_user(self, email, name, birthday, school, is_student, password=None):
        """ 유저를 생성할 때 호출되는 메소드 """
        # 이메일의 '@'이후 부분을 소문자로 바꾼다.
        email = self.normalize_email(email)
        # 연결된 User Model 클래스에 기반하여, 새로운 User 인스턴스를 만든다.
        user = self.model(email=email, name=name, birthday=birthday, school=school, is_student=is_student)
        # AbstractBaseUser 클래스에서 제공하는 set_password 메소드를 사용한다.
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, birthday, school, is_student, password):
        """ 슈퍼유저를 생성하는 메소드 """
        user = self.create_user(email, name, birthday, school, is_student, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(PermissionsMixin, AbstractBaseUser):
    """ 시스템 사용자를 위한 데이터베이스 모델 """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    birthday = models.DateField()
    
    is_student = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # 반드시 생성한 커스텀 유저 매니저를 objects 속성에 등록해주어야한다!
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'birthday', 'school', 'is_student']

    def get_full_name(self):
        """ 사용자의 성과 이름을 가져온다. """
        return self.name

    def get_short_name(self):
        """ 사용자의 이름만 가져온다. """
        return self.name

    def __str__(self):
        """ 사용자 모델을 문자열로 반환한다. """
        return self.email

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name = '사용자 프로필'
        verbose_name_plural = '사용자 프로필'

    def __str__(self):
        return self.nickname

