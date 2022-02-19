from django.shortcuts import render
from rest_framework.views import APIView
from .models import Content, Reply
from rest_framework.response import Response
from user.models import User
import os
from sttalk.settings import MEDIA_ROOT
from uuid import uuid4
from common.common import CommonResponse, SuccessResponse, SuccessResponseWithData, ErrorResponse
from pykrx import stock
import pandas as pd
from datetime import datetime, timedelta


# Create your views here.

class Main(APIView):
    def get(self, request, page):
        Contents = Content.objects.all().order_by('-id')

        email = request.session.get('email', None)
        if email is None:
            return render(request, "user/login.html")
        nickname = User.objects.filter(email=email).first()
        if nickname is None:
            return render(request, "user/login.html")

        #page
        pageNumber = page
        if page > 0:
            prepage = page-1
        else:
            prepage = 0
        nextpage = page+1

        isLastPage = True
        if pageNumber is not None and pageNumber >= 0:
            if Contents.count() <= 15:
                pass
            elif Contents.count() <= (1 + pageNumber) * 15:
                Contents = Contents[pageNumber * 15:]
            else:
                isLastPage = False
                Contents = Contents[pageNumber * 15:(1 + pageNumber) * 15]
        else:
            pass
        ContentList = []
        for i in Contents:
            ContentList.append(dict(
                id=i.id,
                title=i.title,
                content=i.content,
                image=i.image,
                nickname=i.nickname
            ))
        return render(request, "content/main.html", context=dict(ContentList=ContentList, isLastPage=isLastPage, page=page, prepage=prepage, nextpage=nextpage))




class CreateMain(APIView):
    def post(self, request):
        #로그인 세션인증
        email = request.session.get('email', None)
        if email is None:
            return ErrorResponse("정보를 찾을 수 없음 로그인을 하세요.")
        nickname = User.objects.filter(email=email).first()
        if nickname is None:
            return ErrorResponse("유저정보를 찾을 수 없음.")

        title = request.data.get('title')
        content = request.data.get('content')
        stock = request.data.get('stock')
        file = request.data.get('file')
        if file:
            file = request.FILES['file']
            uuid_name = uuid4().hex
            save_path = os.path.join(MEDIA_ROOT, uuid_name)

            with open(save_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            image = uuid_name
        else:
            image = request.data.get('image', '')

        Content.objects.create(content=content, title=title, image=image, nickname=nickname,stock=stock)

        return SuccessResponse()



class Detail(APIView):
    def get(self, request, id):
        #로그인
        email = request.session.get('email', None)
        if email is None:
            return render(request, "user/login.html")
        nickname = User.objects.filter(email=email).first()
        if nickname is None:
            return render(request, "user/login.html")


        detailContent = Content.objects.filter(id=id)

        ContentList = []
        for i in detailContent:
            ContentList.append(dict(
                title=i.title,
                content=i.content,
                image=i.image,
                nickname=i.nickname,
                stock=i.stock
            ))

        ##리플
        replyObjectList = Reply.objects.filter(contentId=id).order_by('-id')
        replyList = []
        for reply in replyObjectList:
            replyList.append(dict(replycontent=reply.replycontent,
                                  nickname=reply.nickname,
                                  replyid=reply.id,
                                  date=reply.date
                                  ))


        ##주가정보
        stockkey = ContentList[0]['stock']
        if len(stockkey) < 1:
            stockkor = ""
            nowprice = "종목번호가 없습니다."
            nowtrade = ""
        elif len(stockkey) == 6:
            df = stock.get_market_cap_by_date(datetime.now() - timedelta(days=5), datetime.now() - timedelta(days=1),
                                            stockkey)
            df = pd.DataFrame(df)
            vol = df['시가총액']
            ratio = df['거래대금']
            trade = df['거래량']

            vol_list = []
            ratio_list = []
            trade_list = []

            for i in vol.values:
                vol_list.append(i)

            for i in ratio.values:
                ratio_list.append(i)

            for i in trade.values:
                trade_list.append(i)

            nowvol = vol_list[len(vol_list) - 1]  ###현재 시총
            nowratio = ratio_list[len(ratio_list) - 1]  ##현재 거래 대금
            nowtrade = trade_list[len(trade_list) - 1]  ##현재 거래량

            nowprice = str(nowratio // nowtrade)+" 원"
            nowtrade = str(nowtrade)+" 건"

            strnowvol = str(nowvol)
            if len(strnowvol) >= 13:
                stockkor = strnowvol[:-12]+"조"+strnowvol[-12:-8]+"억 원"
            else:
                stockkor = strnowvol[:-8]+"억"+strnowvol[-8:-7]+"천만 원"
        else:
            stockkor = "Error!!"
            nowprice = "해당 게시글에 잘못된 종목정보가 입력되었습니다."
            nowtrade = "Error!!"

        return render(request, "content/detail.html", context=dict(ContentList=ContentList, replyList=replyList, contentid=id, stockkor=stockkor, nowprice=nowprice, nowtrade=nowtrade))




class UploadReply(APIView):
    def post(self, request):

        id = request.data.get('id', None)

        if Content.objects.filter(id=id).first() is None:
            return ErrorResponse("글을 찾을 수 없음")
        replycontent = request.data.get('replycontent', None)
        email = request.session.get('email', None)
        if email is None:
            return ErrorResponse("유저 정보를 찾을 수 없음 로그인을 하세요.")
        nickname = User.objects.filter(email=email).first()
        if nickname is None:
            return ErrorResponse("유저정보가 잘못되었음.")


        Reply.objects.create(contentId=id, replycontent=replycontent, nickname=nickname)
        return SuccessResponse()

class DeleteReply(APIView):
    def post(self, request):

        email = request.session.get('email', None)
        if email is None:
            return ErrorResponse("정보를 찾을 수 없음 로그인을 하세요.")
        nickname = User.objects.filter(email=email).first()
        if nickname is None:
            return ErrorResponse("유저정보를 찾을 수 없음.")

        replyid = request.data.get('replyid')
        reply = Reply.objects.get(id=replyid)
        if str(reply.nickname) == str(nickname):
            if reply:
                reply.delete()
            return SuccessResponse()
        else:
            return ErrorResponse("작성자만 삭제 가능합니다.")