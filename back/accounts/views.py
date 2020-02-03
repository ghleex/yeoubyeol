from django.http import HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .serializers import UserCreationSerializer, UserSerializer, WaitingSerializer
from .models import User, Waiting
from .forms import WaitingForm, CustomUserCreationForm
from rest_framework.views import APIView
from datetime import datetime, timedelta, timezone
from string import punctuation, ascii_letters, digits

import random
import secrets

User = get_user_model()

# Create your views here.
class AccountList(APIView):
    # 유저 리스트 조회
    def post(self, request, format=None):
        users = User.objects.filter(username=request.data.get('email'))
        serializer = UserSerializer(users, many=True)
        print(serializer.data)
        if serializer:
            return Response(serializer.data)
        else:
            return Response({'message': '아이디 또는 비밀번호를 다시 확인하세요.'}, status=status.HTTP_204_NO_CONTENT)

    # 유저 정보 수정
    def put(self, request, format=None):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 유저 삭제
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST',])
def email_auth(request):
    waitings = Waiting.objects.all()
    for waiting in waitings:
        if waiting.created_at < datetime.now() - timedelta(minutes=30):
            waiting.delete()
    username = request.data.get('username')
    print(username)
    email = Waiting.objects.filter(username=username)
    if not email:
        serializer = WaitingSerializer(
            data={
                'username': request.data.get('username'),
                'secret_key': secrets.token_urlsafe(50)
            }
        )
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user_email = user.username
            mail_subject = '[SOT] 회원가입 인증 메일입니다.'
            message = render_to_string('accounts/mail_template.html', {'user': user})

            email = EmailMessage(mail_subject, message, to=[user_email])
            email.content_subtype = 'html'
            email.send()
            home = request.data.get('username').split('@')[1]
            return HttpResponse(
                    '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
                        'justify-content: center; align-items: center;">'
                        '입력하신 이메일<span>로 인증 링크가 전송되었습니다. 30분 내에 가입을 완료해 주세요.</span>'
                        '</div>'
            )
    else:
        return HttpResponseBadRequest()


@api_view(['POST',])
def social_auth(request):
    print(request.POST.get('idtoken'))
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
            request.POST.get('idtoken'),
            requests.Request(),
            '832271626552-sj6lpm4cjdd7k5n1vg7lv49ore7ll2q5.apps.googleusercontent.com'
        )
        print(idinfo)
        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        User = get_user_model()
        targetUser = User.objects.filter(username=idinfo['email'])
        if len(targetUser):
            print('Geeeeeeeeeee')
        else:
            newUser = User(username=idinfo['email'], email=idinfo['email'], nickname=idinfo['email'])
            newUser.set_password(idinfo['sub'] + 'salt')
            newUser.save()
            print(newUser)
            print('Baaaaaaaaaaaa')

    except ValueError:
        # Invalid token
        return HttpResponseBadRequest
    return Response('hi')



@api_view(['POST'])
@permission_classes((AllowAny, ))
def user_signup(request, secret_key):
    waiting = get_object_or_404(Waiting, secret_key=secret_key)

    if waiting and waiting.created_at > datetime.now() - timedelta(minutes=30):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            waiting.delete()
            # print(serializer.data)
            return Response({'message': '회원가입이 성공적으로 완료되었습니다.'})

    else:
        waiting.delete()
        return HttpResponse(
            '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
            'justify-content: center; align-items: center;">'
            '토큰값이 유효하지 않습니다.'
            '</div>'
        )


@api_view(['GET'])
def user_detail(request):
    user = get_object_or_404(User, username=username)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST',])
def find_pwd(request):
    username = request.data.get('username')
    user = get_object_or_404(User, username=username)

    symbols = ascii_letters + digits + punctuation
    secure_random = secrets.SystemRandom()
    new_pwd = ''.join(secure_random.choice(symbols) for i in range(10))
    user.password = new_pwd
    user.save()
    
    mail_subject = '[SOT] 임시 비밀번호 메일입니다.'
    user_email = user.username
    message = render_to_string('accounts/find_pwd.html', { 'new_pwd': new.pwd })
    email = EmailMessage(mail_subject, message, to=[user_email])
    email.content_subtype = 'html'
    email.send()
    
    return Response({'message': '메일을 전송했습니다.'})


@api_view(['PUT',])
@login_required
def change_pwd(request):
    username = request.data.get('username')
    user = get_object_or_404(User, username=username)
    serializer = UserCreationSerializer(user)
    if serializer.password == request.data.get('old_password'):
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('new_password'))
            user.save()
            return Response({'message': '비밀번호가 변경되었습니다.'})
        return Response({'message': '비밀번호 양식을 다시 확인하세요!'})
    return Response({'message': '현재 비밀번호가 틀렸습니다.'})


@api_view(['POST',])
def profile(request):
    nickname = request.data.get('nickname')
    user = get_object_or_404(User, nickname=nickname)
    serializer = UserSerializer(user)
    return Response(serializer.data)