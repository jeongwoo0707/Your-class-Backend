from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser, Profile


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = [
        'id',
        'email',
        'name',
        'birthday',
        'date_joined',
        'is_active',
        'is_student',
        'school',
    ]
    # 어드민 페이지에서 유저모델 수정시 보여줄 필드를 지정한다.
    fieldsets = (
        # ('섹션명', '섹션에 포함될 필드')
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'birthday','school',)}),
        ('Permissions', {'fields': ('is_admin', 'is_student' )}),
        ('Important Dates', {'fields': ('last_login', )}),
    )
    # 어드민 페이지에서 신규 유저 생성시 보여줄 필드를 지정한다. (기본으로 username 사용하므로 수정 필요!)
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2')
        }),
        ('Personal Info', {'fields': ('name', 'birthday', )}),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'nickname'
    ]
    fieldsets = (
        # ('섹션명', '섹션에 포함될 필드')
        (None, {'fields': ('nickname', 'avatar')}),
    )


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(Group)