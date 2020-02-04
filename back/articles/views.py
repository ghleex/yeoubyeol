from django.core.mail import EmailMessage
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ArticleSerializer
from .models import Article
from accounts.models import Notification, User
from accounts.serializers import UserSerializer, NotificationSerializer
import secrets, json

# Create your views here.
class ArticleList(APIView):
    # 글 생성 request = 'username', 
    def post(self, request, format=None):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        followers = username.followers.all()
        for follower in followers:
            receive_user = User.object.filter(id=follower)
            notification = {
                'username': receive_user.nickname,
                'message': user.nickname + "님이 새 글을 작성했습니다.",
                'send_user': user.nikename
            }
            json_noti = json.dumps(notification)
            noti_serializer = NotificationSerializer(data=json_noti)
            noti_serializer.save()
            print(noti_serializer.data)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # 글 리스트 조회
    def get(self, request, format=None):
        queryset = Article.objects.all()
        serializer = ArticleSerializer(queryset, many=True)

        return Response(serializer.data)


# 글 상세보기
class ArticleDetail(APIView):
    def get_objects(self, pk):
        try: return Article.objects.get(pk=pk)
        except: raise Http404

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 유저 검색
class SearchResultList(APIView):
    def post(self, request, format=None):
        User = get_user_model()
        query = request.POST.get('keyword')
        print(query)
        if query:
            nicknames = User.objects.filter(nickname__icontains=query)
            nicknames_serializer = UserSerializer(nicknames, many=True)
            words = Article.objects.filter(content__icontains=query)
            words_serializer = ArticleSerializer(words, many=True)
            message = '검색 내용이 없습니다.'
            
            if not (nicknames_serializer and words_serializer):
                return Response({'message': '검색 결과가 존재하지 않습니다.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({
                    'nicknames_serializer_data': nicknames_serializer.data if nicknames_serializer.data else 0,
                    'words_serializer_data': words_serializer.data if words_serializer.data else 0,
                    })
        else:
            return Response({'message': '검색 내용이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)


# Following(Front와 연결하여 확인 필요)
class FollowerList(APIView):
    # 팔로우 신청
    # @login_required
    def post(self, request, format=None):
        me = get_object_or_404(get_user_model(), nickname=request.data.get('my_nickname'))
        you = get_object_or_404(get_user_model(), nickname=request.data.get('your_nickname'))
        serializer = UserSerializer(you)
        if me != you:
            # if serializer.data.followers.filter(pk=me.id).exists():
            if me.id in serializer.data.get('followers'):
                serializer.data.get('followers').remove(me.id)
                # serializer.data.followers.remove(me.id)
            else:
                notification = {
                    'nickname': you.nickname,
                    'message': me.nickname + '님이 팔로우를 신청했습니다.',
                    'send_user': me.nickname
                }
                json_noti = json.dumps(notification)
                noti_serializer = NotificationSerializer(data=json_noti)
                if noti_serializer.is_valid(): noti_serializer.save()

                serializer.data.get('followers').append(me.id)

        serializer = UserSerializer(you, data=serializer.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    # 팔로워 목록
    def get(self, request, user_pk, format=None):        
        person = get_object_or_404(get_user_model(), pk=request.user.pk)
        serializer = UserSerializer(person, many=True)
        if serializer:
            return Response(serializer.data.get('followers'))
        else:
            return Response({'message': '팔로워를 찾을 수 없습니다.'}, status=status.HTTP_204_NO_CONTENT)


class FollowingList(APIView):
    # 팔로잉 목록
    @login_required
    def get(self, request, user_pk, format=None):
        person = get_object_or_404(get_user_model(), pk=request.user.pk)
        serializer = UserSerializer(person, many=True)
        if serializer:
            return Response(serializer.data.get('followings'))
        else:
            return Response({'message': '팔로잉하는 사람이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)


@login_required
def like(request):
    # 요청 보낸 유저 정보
    username = request.data.get('username')
    user = get_object_or_404(User, username=username)
    # 좋아요 한 글
    article = get_object_or_404(Article, article=request.data.get('article'))
    serializer = ArticleSerializer(article)
    if serializer.like_users.filter(pk=user.id).exists():
        serializer.like_users.remove(user)
    else:
        serializer.like_users.add(user)
        like_users = article.like_users.all()
        for like_user in like_users:
            # 알림 받는 유저
            receive_user = get_object_or_404(User, id=like_user)
            notification = {
                'username': receive_user.nickname,
                'message': user.nickname + "님이" + receive_user.nickname + "님의 글을 좋아합니다.",
                'send_user': user.nickname
            }
            json_noti = json.dumps(notification)
            noti_serializer = NotificationSerializer(data=json_noti)
            noti_serializer.save()
    return Response(serializer.data)

