from django.http import HttpResponse
# HttpResponse: ()안의 내용을 전달
from django.shortcuts import render
# render: html 파일을 보여주는 역할


def base_response(request):
    return HttpResponse("안녕하세요! 장고의 시작입니다!")

def first_view(request):
    return render(request, 'my_test.html')