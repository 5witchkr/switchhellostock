from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.

class User(AbstractBaseUser):
    """
        유저 닉네임
        유저 이메일주소(id)
        유저 비밀번호
    """
    nickname = models.CharField(max_length=24, unique=True)
    email = models.EmailField(max_length=40, unique=True)

    USERNAME_FIELD = 'nickname'

    class Meta:
        db_table = "User"