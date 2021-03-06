from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import check_password
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from articles.models import Article
from .serializers import UserCreationSerializer, UserSerializer, WaitingSerializer, AccountCookieSerializer, NotificationSerializer
from .models import User, Waiting, AccountCookie, Notification
from datetime import datetime, timedelta
from string import punctuation, ascii_letters, digits
import random
import secrets
import hashlib
from google.oauth2 import id_token
from google.auth.transport import requests


User = get_user_model()
# Create your views here.


# (Receive token by HTTPS POST)
# ...
class NotificationList(APIView):
    """
        알림센터

        ---
    """
    def get_object(self, pk):
        person = User.objects.filter(id=pk)
        user_notis = Notification.objects.filter(nickname=person[0].id)
        return user_notis
    
    def get_noti(self, pk):
        noti = Notification.objects.filter(id=pk)
        return noti[0]

    def get(self, request, pk, format=None):
        user_notis = self.get_object(pk)
        noti_ids, send_nicknames, notis, pic = [], [], [], []
        cnt = 0
        for noti in user_notis:
            if noti:
                cnt += 1
                noti_ids.append(noti.id)
                send_user = User.objects.filter(id=noti.send_user_id)
                send_nicknames.append(send_user[0].nickname)
                serializer = NotificationSerializer(noti)
                notis.append(serializer.data)
                pic.append('/uploads/' + str(send_user[0].pic_name))

        data = {
            'noti_ids': noti_ids,
            'send_nicknames': send_nicknames,
            'notifications': notis,
            'pic_names': pic,
        }
        return Response(data)

    def put(self, request, pk, format=None):
        notis = self.get_noti(pk)
        noti = {
            'id': notis.id,
            'nickname': notis.nickname_id,
            'is_read': True,
            'created_at': notis.created_at,
            'message': notis.message,
            'send_user': notis.send_user_id,
            'article_no': notis.article_no,
        }
        serializer = NotificationSerializer(notis, data=noti)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class NotificationIsLeftList(APIView):
    """
        확인하지 않은 알림 유무 확인

        ---
    """
    def get_object(self, pk):
        obj = Notification.objects.filter(nickname=pk)
        return obj

    def get(self, request, pk, format=None):
        notis = self.get_object(pk)
        not_read = False
        for noti in notis:
            if noti.is_read == 0:
                not_read = True

        ret = {
            'not_read': not_read,
        }
        return Response(ret, status=status.HTTP_200_OK)


class AccountList(APIView):
    """
        로그인 시, 프로필 정보 수정 시 사용

        ---
    """

    def post(self, request, format=None):
        users = User.objects.filter(username=request.data.get('email'))
        serializer = UserSerializer(users, many=True)
        if serializer:
            return Response(serializer.data)
        else:
            return Response({'message': '아이디 또는 비밀번호를 다시 확인하세요.'}, status=status.HTTP_204_NO_CONTENT)

    # 유저 정보 수정
    def put(self, request, format=None):
        data = request.data
        username = data.get('username')
        username = int(username)
        user = get_object_or_404(User, id=username)
        username = user.username
        nickname = data.get('nickname')
        intro = data.get('intro')
        followers = user.followers.all()
        followers_list = []
        for follower in followers:
            followers_list.append(follower.id)
        followings = user.followings.all()
        followings_list = []
        for following in followings:
            followings_list.append(following.id)
        if data.get('pic_name'):
            pic_name = data.get('pic_name')
            data = {
                'username': username,
                'intro': intro,
                'nickname': nickname,
                'pic_name': pic_name,
                'followers': followers_list,
                'followings': followings_list
            }
        else:
            data = {
                'username': username,
                'intro': intro,
                'nickname': nickname,
                'pic_name': user.pic_name,
                'followers': followers_list,
                'followings': followings_list
            }
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(APIView):
    """
        회원 탈퇴 시 사용

        ---
    """
    # 유저 삭제
    def delete(self, request, pk, format=None):
        user = get_object_or_404(User, id=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', ])
def google(request):
    """
        구글 소셜 로그인 시 사용

        ---
    """
    CLIENT_ID = '832271626552-bpmo24c8a7e1s2lfhs1jfl0ena583jt1.apps.googleusercontent.com'
    token = request.POST.get('id_token')
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
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
        userid = idinfo['sub']
        username = idinfo['email']
        account = User.objects.filter(username=username)
        if account:
            serializer = UserSerializer(account[0])
            return Response(serializer.data)
        nickname = idinfo['email']
        email = idinfo['email']
        pic_name = random.randrange(1, 13, 1)
        pic_name = f'accounts/pic_names/{pic_name}.jpg'
        user = User.objects.create_user(username, email=email, nickname=nickname, pic_name=pic_name, social=True, password=None)
        user.set_unusable_password()
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except ValueError:
        # Invalid token
        return Response(status=status.HTTP_101_SWITCHING_PROTOCOLS)


@api_view(['POST',])
def email_auth(request):
    """
        이메일 인증

        ---
    """
    waitings = Waiting.objects.all()
    for waiting in waitings:
        if waiting.created_at < datetime.now() - timedelta(minutes=10):
            waiting.delete()
    username = request.data.get('username')
    user = User.objects.filter(username=username)
    email = Waiting.objects.filter(username=username)
    if not user:
        if not email:
            data={
                'username': username,
                'secret_key': secrets.token_urlsafe(50)
            }
            serializer = WaitingSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user_email = user.username
                mail_subject = '[SOT] 회원가입 인증 메일입니다.'
                message = render_to_string('accounts/email_template.html', {'user': user})
                email = EmailMessage(mail_subject, message, to=[user_email])
                email.content_subtype = "html"
                email.send()
                
                return Response({'message': '인증 메일이 성공적으로 발송되었습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '아직 인증을 완료하지 않은 계정입니다.'}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({'message': '이미 존재하는 계정입니다.'}, status=status.HTTP_202_ACCEPTED)


@api_view(['POST',])
def checknickname(request):
    """
        닉네임 중복 체크

        ---
    """
    nickname = request.data.get('nickname')
    user = User.objects.filter(nickname=nickname)
    if user:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def user_signup(request, secret_key):
    """
        회원가입

        ---
    """
    waiting = get_object_or_404(Waiting, secret_key=secret_key)
    if waiting and waiting.created_at > datetime.now() - timedelta(minutes=10):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            pic_name = random.randrange(1, 13, 1)
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.pic_name = f'accounts/pic_names/{pic_name}.jpg'
            user.save()
            waiting.delete()
            return Response({'message': '회원가입이 성공적으로 완료되었습니다.'}, status=status.HTTP_200_OK)
    else:
        waiting.delete()
        return Response({'message': '인증 메일을 다시 요청해주세요.'}, status=status.HTTP_202_ACCEPTED)


@api_view(['POST', ])
def check_is_logged_in(request):
    """
        로그인 여부 확인

        ---
    """
    username = request.data.get('username')
    token_1 = request.data.get('token_1')
    account = AccountCookie.objects.filter(username=username)
    if not account:
        token_2 = secrets.token_urlsafe(50)
        data = {
                'username': username,
                'token_1': token_1,
                'token_2': token_2,
            }
        serializer = AccountCookieSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    else:
        account = account[0]
        if not request.data.get('token_2'):
            account.token_1 = request.data.get('token_1')
            data = {
                'username': account.username,
                'token_1': account.token_1,
                'token_2': account.token_2
            }
            serializer = AccountCookieSerializer(account, data=data)
            token_2 = secrets.token_urlsafe(50)
            serializer.token_2 = token_2
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            re_token_1 = request.data.get('token_1')
            re_token_2 = request.data.get('token_2')
            if re_token_1 == account.token_1 and re_token_2 == account.token_2:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    """
        로그아웃

        ---
    """
    username = request.data.get('username')
    account = get_object_or_404(AccountCookie, username=username)
    account.delete()
    return Response({'message': '삭제 성공이다!!'})


@api_view(['POST',])
def findpwd(request):
    """
        비밀번호 찾기

        ---
    """
    username = request.data.get('username')

    user = get_object_or_404(User, username=username)

    symbols = ascii_letters + digits + punctuation
    new_pwd = ''.join(secrets.SystemRandom().choice(symbols) for i in range(10))
    user.set_password(new_pwd)
    user.save()
    
    mail_subject = '[SOT] 임시 비밀번호 메일입니다.'
    user_email = user.username
    message = render_to_string('accounts/find_pwd.html', { 'new_pwd': new_pwd })
    email = EmailMessage(mail_subject, message, to=[user_email])
    email.content_subtype = "html"
    email.send()
    
    return Response({'message': '메일을 전송했습니다.'})


@api_view(['POST', ])
def checkpwd(request):
    """
        비밀번호 변경 전 현재 비밀번호 확인

        ---
    """
    nickname = request.data.get('nickname')
    user = get_object_or_404(User, nickname=nickname)
    password = request.data.get('password')
    if user.check_password(password):
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def changepwd(request):
    """
        비밀번호 변경

        ---
    """
    nickname = request.data.get('nickname')
    password = request.data.get('password')
    user = get_object_or_404(User, nickname=nickname)
    user.set_password(password)
    user.save()
    return Response({'message': '비밀번호가 변경되었습니다.'}, status=status.HTTP_200_OK)


# 타 유저 프로필 조회
@api_view(['POST',])
def profile(request):
    """
        다른 사용자 프로필 조회

        ---
    """
    nickname = request.data.get('nickname')
    user = get_object_or_404(User, nickname=nickname)
    serializer = UserSerializer(user)
    articles = Article.objects.filter(author=user.id)
    like_nums = 0
    for article in articles:
        like_nums += len(article.like_users.all())
    data = {
        'id': serializer.data.get('id'),
        'nickname': serializer.data.get('nickname'),
        'intro': serializer.data.get('intro'),
        'pic_name': serializer.data.get('pic_name'),
        'username': serializer.data.get('username'),
        'followers': serializer.data.get('followers'),
        'followings': serializer.data.get('followings'),
        'like_nums': like_nums
    }
    return Response(data)
