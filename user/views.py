from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from django.contrib.auth.hashers import make_password, check_password
import logging
from common.common import CommonResponse, SuccessResponse, SuccessResponseWithData, ErrorResponse
from django.shortcuts import render


# Create your views here.


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        userEmail = User.objects.filter(email=email).first()
        if userEmail is None:
            return ErrorResponse("회원정보가 잘못되었습니다.")
        if check_password(password, userEmail.password):
            request.session['email'] = email
            return SuccessResponse()
        else:
            return ErrorResponse("회원정보가 잘못되었습니다.")

class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        # logger.info("Test RegistUser API START!!!!")
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        nickname = request.data.get('nickname', None)
        print(email)
        print(password)
        print(nickname)

        if User.objects.filter(email=email).exists():
            return ErrorResponse('해당 이메일 주소가 존재합니다.')
        elif User.objects.filter(nickname=nickname).exists():
            return ErrorResponse('사용자 닉네임 "' + nickname + '"이(가) 존재합니다.')

            # make_password(password)
        User.objects.create(password=make_password(password),
                            email=email,
                            nickname=nickname)
        # logger.info("Test RegistUser API END!!!!")
        return SuccessResponseWithData("회원가입 성공했습니다. 로그인 해주세요.")


class Logout(APIView):
    def post(self, request):
        request.session.flush()
        return render(request, "user/login.html")