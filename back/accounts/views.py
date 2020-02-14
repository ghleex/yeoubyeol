from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from articles.models import Article
from .serializers import UserCreationSerializer, UserSerializer, WaitingSerializer, AccountCookieSerializer
from .models import User, Waiting, AccountCookie
from .forms import WaitingForm, CustomUserCreationForm
from datetime import datetime, timedelta
from string import punctuation, ascii_letters, digits
import random
import secrets

User = get_user_model()
# Create your views here.
class AccountList(APIView):
    # 유저 리스트 조회(영자님 전용)
    def post(self, request, format=None):
        users = User.objects.filter(username=request.data.get('email'))
        serializer = UserSerializer(users, many=True)
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
                print(user_email)
                mail_subject = '[SOT] 회원가입 인증 메일입니다.'
                message = render_to_string('accounts/mail_template.html', {'user': user})
                email = EmailMessage(mail_subject, message, to=[user_email])
                email.content_subtype = "html"
                email.send()
                
                return Response({'message': '인증 메일이 성공적으로 발송되었습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '아직 인증을 완료하지 않은 계정입니다.'}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({'message': '이미 존재하는 계정입니다.'}, status=status.HTTP_202_ACCEPTED)

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
            pass
            # print('Geeeeeeeeeee')
        else:
            newUser = User(username=idinfo['email'], email=idinfo['email'], nickname=idinfo['email'])
            newUser.set_password(idinfo['sub'] + 'salt')
            newUser.save()
            # print(newUser)
            # print('Baaaaaaaaaaaa')

    except ValueError:
        # Invalid token
        return HttpResponseBadRequest
    return Response('hi')


@api_view(['POST',])
def checknickname(request):
    nickname = request.data.get('nickname')
    print(nickname)
    user = User.objects.filter(nickname=nickname)
    print(user)
    if user:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def user_signup(request, secret_key):
    waiting = get_object_or_404(Waiting, secret_key=secret_key)
    if waiting and waiting.created_at > datetime.now() - timedelta(minutes=10):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(request.data.get('password'))
            pic_name = random.randrange(1, 13, 1)
            user.pic_name = 'accounts/pic/{pic_name}.png'
            user.save()
            waiting.delete()
            return Response({'message': '회원가입이 성공적으로 완료되었습니다.'}, status=status.HTTP_200_OK)
    else:
        waiting.delete()
        return Response({'message': '인증 메일을 다시 요청해주세요.'}, status=status.HTTP_202_ACCEPTED)

@api_view(['POST', ])
def check(request):
    account = AccountCookie.objects.filter(username=request.data.get('username'))
    username = request.data.get('username')
    token_1 = request.data.get('token_1')
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
            print(account.token_1)
            account.token_1 = request.data.get('token_1')
            print(account.token_1)
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
    username = request.data.get('username')
    account = get_object_or_404(AccountCookie, username=username)
    account.delete()
    return Response({'message': '삭제 성공이다!!'})

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
    new_pwd = ''.join(secrets.SystemRandom().choice(symbols) for i in range(10))
    # print(new_pwd)
    user.set_password(new_pwd)
    user.save()
    
    mail_subject = '[SOT] 임시 비밀번호 메일입니다.'
    user_email = user.username
    message = render_to_string('accounts/find_pwd.html', { 'new_pwd': new_pwd })
    email = EmailMessage(mail_subject, message, to=[user_email])
    email.content_subtype = "html"
    email.send()
    
    return Response({'message': '메일을 전송했습니다.'})


@api_view(['PUT',])
def change_pwd(request):
    username = request.data.get('username')
    user = get_object_or_404(User, username=username)
    serializer = UserCreationSerializer(user)
    if serializer.password == request.data.get('old_password'):
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('new_password'))
            user.save()
            return Response({'message': '비밀번호가 변경되었습니다.'}, status=status.HTTP_200_OK)
        return Response({'message': '비밀번호 양식을 다시 확인하세요!'}, status=status.HTTP_202_ACCEPTED)
    return Response({'message': '현재 비밀번호가 틀렸습니다.'})


# 타 유저 프로필 조회
@api_view(['POST',])
def profile(request):
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
