from django.core.mail import EmailMessage
from django.http import Http404, HttpResponse
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
        print(request.data)
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
            response = HttpResponse(serializer.data)
            response.set_cookie('AUTH_TOKEN', request.data.get('token'))
            return response
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
    like_articles = Article.objects.all()
    datas = []
    like_datas = []
    for like_article in like_articles:
        if like_article.like_users.filter(id=account.id).exists():
            like_article_comments = like_article.comment_set.all()
            like_article_serializer = ArticleSerializer(like_article)
            like_data = like_article_serializer.data
            like_article_author = like_article_serializer.data.get('author')
            like_article_user = get_object_or_404(User, id=like_article_author)
            like_data['pic_name'] = like_article_user.pic_name
            for u in range(len(like_data.get('hashtags'))):
                hashtag = get_object_or_404(Hashtag, id=like_data.get('hashtags')[u])
                like_data.get('hashtags')[u] = hashtag.hashtag
            like_data['nickname'] = like_article_user.nickname
            like_data['comments'] = len(like_article_comments)
            like_datas.append(like_data)
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
    result = {
        'my_articles': datas,
        'like_articles': like_datas,
    }
    return Response(result)

# 글 상세보기
class ArticleDetail(APIView):
    # 글 상세보기
    def get(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        serializer = ArticleSerializer(article)
        user = get_object_or_404(User, id=serializer.data.get('author'))
        comments = article.comment_set.all()
        data = []
        hashtags = serializer.data.get('hashtags')
        hashtag_list = []
        for hashtag in range(len(hashtags)):
            hashs = get_object_or_404(Hashtag, id=hashtags[hashtag])
            hashtag_list.append(hashs.hashtag)
        for comment in comments:
            comment_serializer = CommentSerializer(comment)
            author = comment_serializer.data.get('author')
            user = get_object_or_404(User, id=author)
            data.append([user.nickname, user.pic_name,comment.id, comment.comment, comment.created_at])
        result = {
            'nickname': user.nickname,
            'pic_name': user.pic_name,
            'article': serializer.data,
            'hashtags': hashtag_list,
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
        query = request.data.get('keyword')
        users = User.objects.all()
        data = []
        if query:
            for user in users:
                if query in user.nickname:
                    data.append({
                        'nickname': user.nickname,
                        'pic_name': user.pic_name,
                        'intro': user.intro
                    })
            if len(data) > 0:
                return Response(data)
            else:
                return Response({'message': '검색 결과가 없습니다.'}, status=status.HTTP_204_NO_CONTENT)
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
    print('--------------------')
    print(request.data)
    print('--------------------')
    nickname = request.data.get('nickname')
    user = get_object_or_404(User, nickname=nickname)
    # 좋아요 한 글
    article = get_object_or_404(Article, id=request.data.get('article_id'))
    like_users = article.like_users.all()
    article_like_users = []
    article_hashtags = []
    for like_user in like_users:
        article_like_users.append(like_user.id)
    hashtags = article.hashtags.all()
    for hashtag in hashtags:
        article_hashtags.append(hashtag.id)
    ar_data = {
        'article': article.article,
        'author': article.author_id,
        'like_users': article_like_users,
        'hashtags': article_hashtags,
        'image': article.image
    }
    serializer = ArticleSerializer(article, data=ar_data)
    if len(article.like_users.all()) == 30000:
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
    if serializer.is_valid():
        article = serializer.save()
        if article.like_users.filter(id=user.id).exists():
            # index = serializer.data.get('like_users').index(user.id)
            article.like_users.remove(user.id)
        else:
            article.like_users.add(user.id)
            like_users = article.like_users.all()
            for like_user in like_users:
                # 알림 받는 유저
                user  = get_object_or_404(User, username=like_user)
                receive_user = get_object_or_404(User, id=user.id)
                notification = {
                    'nickname': receive_user.nickname,
                    'message': user.nickname + "님이" + receive_user.nickname + "님의 글을 좋아합니다.",
                    'send_user': user.nickname
                }
                noti_serializer = NotificationSerializer(data=notification)
                if noti_serializer.is_valid():
                    notification = noti_serializer.save()
                    notification.save()
        article.save()
        return Response(serializer.data)


class CommentList(APIView):
    # 댓글 작성
    def post(self, request):
        # request = my_nickname, article_author, comment
        article_id = request.data.get('article_id')
        my_nickname = request.data.get('my_nickname')
        comment = request.data.get('comment')
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
        noti_serializer = NotificationSerializer(data=notification)
        if noti_serializer.is_valid():
            noti = noti_serializer.save()
            noti.save()
        if serializer.is_valid():
            comment = serializer.save()
            comment.save()
            return Response(serializer.data)
        else:
            return Response({'message': '이런 나쁜 요청'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 댓글 수정
    def put(self, request):
        # request = article_id, comment_id, comment
        comment_id = request.data.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)
        comment.comment = request.data.get('comment')
        comment_data = {
            'article': comment.article_id,
            'author': comment.author_id,
            'comment': comment.comment,
        }
        serializer = CommentSerializer(comment, data=comment_data)
        serializer.comment = request.data.get('comment')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    # 댓글 삭제
    def delete(self, request, pk):
        # request = nickname, comment_id
        comment = get_object_or_404(Comment, id=pk)
        print(comment)
        comment.delete()
        return Response({'message': '댓글이 성공적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


def honor(request): 
    articles = HonorArticle.objects.all()
    serializer = HonorArticleSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['POST', ])
def hashtag(request):
    hashtag_pk = request.data.get('hashtag_pk')
    hashtag = get_object_or_404(Hashtag, id=hashtag_pk)
    articles = hashtag.article_set.order_by('-pk')
    data = {
        'articles': articles,
        'hashtag': hashtag
    }
    return Response(data)
