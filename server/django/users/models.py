import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = RegexValidator(
        regex=r"^[a-zA-Z0-9.@+-]+$", message=_("ユーザー名には半角アルファベット、半角数字、および@/./+/-/_のみ使用できます。")
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        _("username"),
        max_length=15,
        unique=True,
        help_text="この項目は必須です。半角アルファベット、半角数字、@/./+/-/_ で15文字以下にしてください。",
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png")

    def __str__(self):
        return self.username
