
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from base.models import BaseModel
from exchange_rate.models import Country

class Setting(BaseModel):
    MODE_CHOICES = [
        ("light", "light"),
        ("dark", "dark"),
    ]
    mode = models.CharField(
        max_length=10,
        choices=MODE_CHOICES,
        default=MODE_CHOICES[0][0],
        verbose_name="환경 모드",
    )

    class Meta:
        db_table = "setting"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password):
        if not email:
            raise ValueError("must have user email")
        if not password:
            raise ValueError("must have user password")

        user = self.model(email=self.normalize_email(email))
        user.setting = Setting.objects.create()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=self.normalize_email(email), password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create(self, *args, **kwargs):
        user: User = super().create(
            setting=Setting.objects.create(),
            **kwargs
        )
        user.set_unusable_password()
        return user

    def get_and_update_or_create(self, **kwargs) -> tuple["User", bool]:
        email = kwargs.get("email")
        is_create = False
        try:
            user: User = self.model.objects.get(email=email)
            user.field_update(**kwargs)
        except self.model.DoesNotExist:
            user: User = self.model.objects.create(**kwargs)
            is_create = True
        return user, is_create


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    age_range = models.CharField(max_length=10)
    avatar_url = models.CharField(
        max_length=255,
        default="http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_110x110.jpg",
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    refresh_token = models.CharField(max_length=80, null=True)
    setting = models.OneToOneField(Setting, on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = "email"

    @property
    def is_staff(self):
        return self.is_admin

    def field_update(self, **kwargs):
        """
        기존 사용자와 다른 값이 존재하면 갱신
        """
        if not kwargs:
            raise TypeError("required model fields ")

        keys: list[str] = list(kwargs.keys())

        is_update = False

        for i in keys:
            if (attr := kwargs.get(i)) != getattr(self, i):
                setattr(self, i, attr)
                is_update = True

        if is_update:
            self.save()

    class Meta:
        db_table = "user"



