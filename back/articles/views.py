from django.core.mail import EmailMessage
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ArticleSerializer, CommentSerializer, HonorArticleSerializer, HashtagSerializer
from .models import Article, Comment, HonorArticle, Hashtag
from accounts.models import Notification, User
from accounts.serializers import UserSerializer, NotificationSerializer
from string import ascii_letters
from konlpy.tag import Okt, Kkma, Komoran, Hannanum
from collections import Counter
# from directmessages.apps import Inbox
import operator
import konlpy
import secrets, json

# Create your views here.
class ArticleList(APIView):
    # 글 생성 request = 'username', 
    def post(self, request, format=None):
        nickname = request.data.get('nickname')
        article = request.POST.get('article')
        hashtags = request.POST.get('hashtags')
        hashtags = hashtags.split(',')
        user = get_object_or_404(User, nickname=nickname)
        data = {
            'article': request.data.get('article'),
            'author': user.id,
            'image': request.data.get('image'),
        }
        serializer = ArticleSerializer(data=data)
        followers = user.followers.all()
        for follower in followers:
            follower_user = get_object_or_404(User, id=follower.id)
            notification = {
                    'nickname': follower_user.nickname,
                    'message': user.nickname + "님이 새 글을 작성했습니다.",
                    'send_user': user.nickname
                }
            noti_serializer = NotificationSerializer(data=notification)
            if noti_serializer.is_valid():
                noti = noti_serializer.save()
                noti.save()
        if serializer.is_valid():
            article = serializer.save()
            for word in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(
                    hashtag=word)
                hash_serializer = HashtagSerializer(data=hashtag)
                if hash_serializer.is_valid():
                    hash_serializer.save()
                article.hashtags.add(hashtag)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST',])
def mainfeed(request):
    nickname = request.data.get('nickname')
    user = get_object_or_404(User, nickname=nickname)
    serializer = UserSerializer(user)
    datas = []
    for following in serializer.data.get('followings'):
        articles = Article.objects.filter(author=following)
        for article in articles:
            comments = article.comment_set.all()
            article_serializer = ArticleSerializer(article)
            account = get_object_or_404(User, id=article_serializer.data.get('author'))
            data = article_serializer.data
            data['pic_name'] = account.pic_name
            for u in range(len(data['hashtags'])):
                hashtag = get_object_or_404(Hashtag, id=data['hashtags'][u])
                data['hashtags'][u] = hashtag.hashtag
            data['nickname'] = account.nickname
            data['comments'] = len(comments)
            datas.append(data)
    return Response(datas)


@api_view(['POST', ])
def recommend(request):
    content = request.data.get('article')
    okt = Hannanum()
    keywords = okt.nouns(request.POST.get('article'))
    count = Counter(keywords)
    count = sorted(sorted(count.items(), key=operator.itemgetter(0)), key=lambda x: x[1], reverse=True) 
    data = []
    for k in count:
        data.append(k[0])
        if len(data) > 2:
            break
    return Response(data)
        

# 나의 글 보기
@api_view(['POST', ])
def myarticle(request):
    nickname = request.data.get('nickname')
    account = get_object_or_404(User, nickname=nickname)
    articles = Article.objects.filter(author=account.id)
    datas = []
    for article in articles:
        comments = article.comment_set.all()
        article_serializer = ArticleSerializer(article)
        data = article_serializer.data
        data['pic_name'] = account.pic_name
        for u in range(len(data['hashtags'])):
            hashtag = get_object_or_404(Hashtag, id=data['hashtags'][u])
            data['hashtags'][u] = hashtag.hashtag
        data['nickname'] = account.nickname
        data['comments'] = len(comments)
        datas.append(data)
    return Response(datas)

# 글 상세보기
class ArticleDetail(APIView):
    # 글 상세보기
    def get(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        serializer = ArticleSerializer(article)
        user = get_object_or_404(User, id=serializer.data.get('author'))
        comments = article.comment_set.all()
        data = []
        for comment in comments:
            comment_serializer = CommentSerializer(comment)
            author = comment_serializer.data.get('author')
            user = get_object_or_404(User, id=author)
            data.append([user.nickname, user.pic_name, comment.comment, comment.created_at])
        result = {
            'nickname': user.nickname,
            'pic_name': user.pic_name,
            'article': serializer.data,
            'comments': data
        }
        return Response(result)

    # 글 수정
    def put(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 글 삭제
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
            print('--------------------------')
            print(serializer.data.get('followers'))
            print(me.id)
            print('--------------------------')
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
                if noti_serializer.is_valid(): 
                    noti = noti_serializer.save()
                    noti.save()
                serializer.data.get('followers').append(me.id)

        serializer = UserSerializer(you, data=serializer.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    # 팔로워 목록
    def get(self, request, format=None):        
        person = get_object_or_404(get_user_model(), id=request.data.get('user_id'))
        serializer = UserSerializer(person, many=True)
        if serializer:
            return Response(serializer.data.get('followers'))
        else:
            return Response({'message': '팔로워를 찾을 수 없습니다.'}, status=status.HTTP_204_NO_CONTENT)


# 팔로잉 목록
@api_view(['POST', ])
def followinglist(request):
    person = get_object_or_404(get_user_model(), nickname=request.data.get('nickname'))
    serializer = UserSerializer(person)
    users = []
    for user_id in serializer.data.get('followings'):
        user = get_object_or_404(get_user_model(), id=user_id)
        users.append(UserSerializer(user).data)
    if serializer:
        return Response({'data': users})
    else:
        return Response({'message': '팔로잉하는 사람이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', ])
def followerlist(request):
    person = get_object_or_404(get_user_model(), nickname=request.data.get('nickname'))
    serializer = UserSerializer(person)
    users = []
    for user_id in serializer.data.get('followers'):
        user = get_object_or_404(get_user_model(), id=user_id)
        users.append(UserSerializer(user).data)

    if serializer:
        return Response({'data': users})
    else:
        return Response({'message': '팔로워를 찾을 수 없습니다.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', ])
def like(request):
    # 요청 보낸 유저 정보
    username = request.data.get('username')
    user = get_object_or_404(User, username=username)
    # 좋아요 한 글
    article = get_object_or_404(Article, article_id=request.data.get('article_id'))
    serializer = ArticleSerializer(article)
    if len(article.like_uses_set.all()) == 30000:
        data = {
            'article': article.article,
            'author': article.author,
            'hashtags': article.hashtags,
            'image': article.image
        }
        honorserializer = HonorArticleSerializer(data=data)
        honorserializer.save()
        author = article.author
        noti_user = get_object_or_404(User, id=author)
        notification = {
                'nickname': noti_user.nickname,
                'message': noti_user.nickname + "님의 글이 명예의 전당에 올라갔습니다.",
                'send_user': noti_user.nickname
            }
        json_noti = json.dumps(notification)
        noti_serializer = NotificationSerializer(data=json_noti)
        if noti_serializer.is_valid():
            noti_serializer.save()
        article.delete()
    if serializer.like_users.filter(id=user.id).exists():
        serializer.like_users.remove(user)
    else:
        serializer.like_users.add(user)
        like_users = article.like_users.all()
        for like_user in like_users:
            # 알림 받는 유저
            receive_user = get_object_or_404(User, id=like_user)
            notification = {
                'nickname': receive_user.nickname,
                'message': user.nickname + "님이" + receive_user.nickname + "님의 글을 좋아합니다.",
                'send_user': user.nickname
            }
            json_noti = json.dumps(notification)
            noti_serializer = NotificationSerializer(data=json_noti)
            noti_serializer.save()
    return Response(serializer.data)



class CommentList(APIView):
    # 댓글 작성
    def post(self, request):
        # request = my_nickname, article_author, comment
        article_id = request.data.get('article_id')
        my_nickname = request.data.get('my_nickname')
        comment = request.data.get('comment')
        print(article_id, my_nickname, comment)
        user = get_object_or_404(User, nickname=my_nickname)
        article = get_object_or_404(Article, id=article_id)
        article_user = get_object_or_404(User, id=article.author_id)
        comment_data = {
            'article': article_id,
            'author': user.id,
            'comment': comment
        }
        serializer = CommentSerializer(data=comment_data)
        notification = {
                'nickname': article_user.nickname,
                'message': user.nickname + "님이" + article_user.nickname + "님의 글에 댓글을 남겼습니다.",
                'send_user': user.nickname
            }
        print(notification)
        noti_serializer = NotificationSerializer(data=notification)
        if noti_serializer.is_valid():
            noti = noti_serializer.save()
            print(noti_serializer.data)
            noti.save()
        if serializer.is_valid():
            comment = serializer.save()
            comment.save()
            print(serializer.data)
            return Response(serializer.data)
        else:
            return Response({'message': '이런 나쁜 요청'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 댓글 수정
    def put(request):
        # request = article_id, comment_id, comment
        article_id = request.data.get('article_id')
        comment_id = request.data.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = CommentSerializer(comment)
        serializer.comment = request.data.get('comment')
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '댓글이 성공적으로 변경되었습니다.'}, serializer.data)

    # 댓글 삭제
    def delete(request):
        # request = nickname, comment_id
        nickname = request.data.get('nickname')
        user = get_object_or_404(User, nickname=nickname)
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = CommentSerializer(comment)
        if user.id == comment.author:
            serializer.delete()
            return Response({'message': '댓글이 성공적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


def honor(request): 
    articles = HonorArticle.objects.all()
    serializer = HonorArticleSerializer(articles, many=True)
    return Response(serializer.data)

def hashtag(request):
    hashtag_pk = request.data.get('hashtag_pk')
    hashtag = get_object_or_404(Hashtag, id=hashtag_pk)
    articles = hashtag.article_set.order_by('-pk')
    data = {
        'articles': articles,
        'hashtag': hashtag
    }
    return Response(data)
    