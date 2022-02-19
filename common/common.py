from rest_framework.views import APIView
from rest_framework.response import Response


class CongView(APIView):
    version = ''

    #헤더영역
    def dispatch(self, request, *args, **kwargs):
        self.version = request.headers.get('version', '1.0')
        return super(CongView, self).dispatch(request, *args, **kwargs)



def CommonResponse(resultCode, resultMsg, data):
    return Response(status=200,
                    data=dict(
                        resultCode=resultCode,
                        resultMsg=resultMsg,
                        data=data
                        )
                    )

def SuccessResponse():
    return Response(status=200,
                    data=dict(
                        resultCode=0,
                        resultMsg="success"
                        )
                    )

def SuccessResponseWithData(data):
    return Response(status=200,
                    data=dict(
                        resultCode=1,
                        resultMsg="success",
                        data=data
                        )
                    )

def ErrorResponse(resultMsg):
    return Response(status=400,
                    data=dict(
                        resultCode=999,
                        resultMsg=resultMsg
                        )
                    )