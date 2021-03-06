from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from base.models import BaseModel
from base.utils import destructuring

from exchange_rate.models import Country


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
        nickname, email, gender, age_range, avatar_url = destructuring(
            kwargs, "nickname", "email", "gender", "age_range", "avatar_url"
        )

        user = super().create(
            email=email,
            nickname=nickname,
            gender=gender,
            age_range=age_range,
            avatar_url=avatar_url,
            setting=Setting.objects.create(),
        )
        user.set_unusable_password()
        return user


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

    def update(self, **kwargs):
        if not kwargs:
            return
        nickname, gender, age_range, avatar_url = destructuring(
            kwargs, "nickname", "gender", "age_range", "avatar_url"
        )

        if self.nickname != nickname:
            self.nickname = nickname

        if self.gender != gender:
            self.gender = gender

        if self.age_range != age_range:
            self.age_range = age_range

        if self.avatar_url != avatar_url:
            self.avatar_url = avatar_url

        self.save()

    class Meta:
        db_table = "user"


class WatchList(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watch_list",
        verbose_name="사용자",
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="국가")

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        db_table = "watch_list"
        ordering = []
