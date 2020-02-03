from django.core.mail import EmailMessage
from django.http import Http404
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ArticleSerializer
from .models import Article
from accounts.serializers import UserSerializer
import secrets

# Create your views here.
class ArticleList(APIView):
    # 글 리스트 생성
    def post(self, request, format=None):
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
    def post(self, request, format=None):
        me = get_object_or_404(get_user_model(), username=request.data.get.my_username)
        you = get_object_or_404(get_user_model(), username=request.data.get.your_username)
        serializer = UserSerializer(you)
        if me != you:
            if serializer.followers.filter(pk=me.pk).exists():
                serializer.followers.remove(me)
            else:
                serializer.followers.add(me)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    # 팔로워 목록
    def get(self, request, user_pk, format=None):        
        person = get_object_or_404(get_user_model(), pk=request.user.pk)
        serializer = UserSerializer(person, many=True)
        if serializer:
            return Response(serializer.data)
        else:
            return Response({'message': '팔로워를 찾을 수 없습니다.'}, status=status.HTTP_204_NO_CONTENT)