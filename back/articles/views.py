from django.http import Http404, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ArticleSerializer, CommentSerializer, HonorArticleSerializer, HashtagSerializer
from .models import Article, Comment, HonorArticle, Hashtag
from accounts.models import Notification, User
from accounts.serializers import UserSerializer, NotificationSerializer
from string import ascii_letters
from collections import Counter
from datetime import datetime
# from directmessages.apps import Inbox
from konlpy.tag import Hannanum
import konlpy
import operator
import secrets, json

# Create your views here.
class ArticleList(APIView):
    # 아래는 삭제 금지
    """
        글을 새롭게 생성할 때 사용할 API

        ---
    """
    
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
        if serializer.is_valid():
            article = serializer.save()
            for word in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(hashtag=word)
                hash_serializer = HashtagSerializer(data=hashtag)
                if hash_serializer.is_valid():
                    hash_serializer.save()
                article.hashtags.add(hashtag)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    

class ArticleDetail(APIView):
    """
        작성한 글 내용을 받고, 수정, 삭제할 때 사용할 API

        ---
    """
    def get_object(self, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        return article

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        user = get_object_or_404(User, id=serializer.data.get('author'))
        comments = article.comment_set.all()
        data = []
        hashtags = serializer.data.get('hashtags')
        hashtag_list = []
        # 해시태그
        for hashtag in range(len(hashtags)):
            hashs = get_object_or_404(Hashtag, id=hashtags[hashtag])
            hashtag_list.append(hashs.hashtag)
        
        # 댓글
        for comment in comments:
            comment_serializer = CommentSerializer(comment)
            author = comment_serializer.data.get('author')
            c_user = get_object_or_404(User, id=author)
            data.append([c_user.nickname, f'/uploads/{c_user.pic_name}' ,comment.id, comment.comment, comment.created_at])
        
        # 최종적으로 보낼 것
        result = {
            'nickname': user.nickname,
            'pic_name': f'/uploads/{user.pic_name}',
            'article': serializer.data,
            'hashtags': hashtag_list,
            'comments': data
        }
        return Response(result)

    def put(self, request, pk, format=None):
        article = self.get_object(pk)
        article.article = request.data.get('article')
        article_hashtags = article.hashtags.all()
        for article_hashtag in article_hashtags:
            article.hashtags.remove(article_hashtag.id)
        if request.data.get('image'):
            article.image = request.data.get('image')
        hashtags = request.data.get('hashtags')
        hashtags = hashtags.split(',')
        
        for word in hashtags:
            hashtag, created = Hashtag.objects.get_or_create(hashtag=word)
            hash_serializer = HashtagSerializer(data=hashtag)
            if hash_serializer.is_valid():
                hash_serializer.save()
            article.hashtags.add(hashtag)
            
        data = {
            'article': article.article,
            'author': article.author_id,
            'image': article.image,
        }
        serializer = ArticleSerializer(article, data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(article.id)

    # 글 삭제
    def delete(self, request, pk, format=None):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(APIView):
    """
        댓글 새로 작성할 때 사용할 API

        ---
    """

    # article 가져오기
    def get_object(self, article_id):
        article = get_object_or_404(Article, id=article_id)
        return article    

    # 가져온 article 에 댓글 작성
    def post(self, request, format=None):
        article = self.get_object(request.data.get('article_id'))
        my_nickname = request.data.get('my_nickname')
        comment = request.data.get('comment')
        user = get_object_or_404(User, nickname=my_nickname)
        article_user = get_object_or_404(User, id=article.author_id)
        comment_data = {
            'article': article.id,
            'author': user.id,
            'comment': comment
        }
        serializer = CommentSerializer(data=comment_data)
        if article_user != user:
            notification = {
                    'nickname': article_user.id,
                    'message': 'CO',
                    'send_user': user.id,
                    'article_no': article.id,
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


class CommentDetail(APIView):
    """
        작성한 댓글을 수정하거나 삭제할 때 사용할 API

        ---
    """

    # 수정/삭제할 댓글 가져오기
    def get_object(self, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        return comment

    # 댓글 수정
    def put(self, request, pk):
        comment = self.get_object(pk)
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

    def delete(self, request, pk):
        comment = self.get_object(pk)
        comment.delete()
        return Response({'message': '댓글이 성공적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', ])
def mainfeed(request):
    """
        내가 팔로우하고 있는 사용자 글을 볼 때 사용할 API

        ---
    """    
    nickname = request.data.get('nickname')
    user = get_object_or_404(User, nickname=nickname)
    serializer = UserSerializer(user)
    start = int(request.data.get('start'))
    datas = []
    for following in serializer.data.get('followings'):
        articles = Article.objects.filter(author=following)
        for article in articles:
            comments = article.comment_set.all()
            article_serializer = ArticleSerializer(article)
            account = get_object_or_404(User, id=article_serializer.data.get('author'))
            data = article_serializer.data
            data['pic_name'] = f'/uploads/{account.pic_name}'
            for u in range(len(data['hashtags'])):
                hashtag = get_object_or_404(Hashtag, id=data['hashtags'][u])
                data['hashtags'][u] = hashtag.hashtag
            data['nickname'] = account.nickname
            data['comments'] = len(comments)
            datas.append(data)
    return Response(datas[start:start+10])


@api_view(['POST', ])
def rec_hashtag(request):
    """
        해시태그 추천 시 사용할 API

        ---
    """
    content = request.data.get('article')
    hannanum = Hannanum()
    keywords = hannanum.nouns(content)
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
    """
        프로필에서 내가 작성한 모든 글을 볼 때 사용할 API

        ---
    """
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
            like_data['pic_name'] = f'/uploads/{like_article_user.pic_name}'
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
        data['pic_name'] = f'/uploads/{account.pic_name}'
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

 

class SearchResultList(APIView):
    """
        유저 검색 시 사용할 API

        ---
    """
    def post(self, request, format=None):
        query = request.data.get('keyword')
        users = User.objects.all()
        data = []
        if query:
            for user in users:
                if query in user.nickname:
                    data.append({
                        'pk': user.id,
                        'nickname': user.nickname,
                        'pic_name': f'/uploads/{user.pic_name}',
                        'intro': user.intro,
                    })
            if len(data) > 0:
                return Response(data)
            else:
                return Response({'message': '검색 결과가 없습니다.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': '검색 내용이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', ])
def follow(request):
    """
        팔로우 신청할 때 사용할 API

        ---
    """
    me = get_object_or_404(get_user_model(), nickname=request.data.get('my_nickname'))
    you = get_object_or_404(get_user_model(), nickname=request.data.get('your_nickname'))
    if me != you:
        if me in you.followers.all():
            you.followers.remove(me)
        else:
            notification = {
                'nickname': you.id,
                'message': 'FL',
                'send_user': me.id,
            }
            noti_serializer = NotificationSerializer(data=notification)
            if noti_serializer.is_valid(): 
                noti = noti_serializer.save()
                noti.save()
            you.followers.add(me)
    serializer = UserSerializer(you)
    return Response(serializer.data)


# 팔로잉 목록
@api_view(['POST', ])
def followinglist(request):
    """
        팔로잉 목록 보기

        ---
    """
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
    """
        팔로워 목록 보기

        ---
    """

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
    """
        좋아요 신청/취소 시 사용할 API

        ---
    """

    # 요청 보낸 유저 정보
    nickname = request.data.get('nickname')
    user = get_object_or_404(User, nickname=nickname)
    # 좋아요 한 글
    article = get_object_or_404(Article, id=request.data.get('article_id'))
    month = datetime.now().month
    if article.month != month:
        article.month = month
        article.popular_post = 0
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
    if serializer.is_valid():
        article = serializer.save()
        if article.like_users.filter(id=user.id).exists():
            article.like_users.remove(user.id)
            if article.popular_post > 0:
                article.popular_post -= 1
        else:
            article.like_users.add(user.id)
            article.popular_post += 1
            
            # 알림 받는 유저
            user = get_object_or_404(User, nickname=nickname)
            receive_user = get_object_or_404(User, id=article.author_id)
            if user != receive_user:
                notification = {
                    'nickname': receive_user.id,
                    'message': 'LK',
                    'send_user': user.id,
                    'article_no': article.id,
                }
                
                noti_serializer = NotificationSerializer(data=notification)
                if noti_serializer.is_valid():
                    notification = noti_serializer.save()
                    notification.save()
        article.save()
    if len(article.like_users.all()) >= 5:
        article_hashtag = []
        for hashtag in article.hashtags.all():
            article_hashtag.append(hashtag.id)
        data = {
            'article': article.article,
            'author': article.author_id,
            'hashtags': article_hashtag,
            'image': article.image
        }
        honorserializer = HonorArticleSerializer(data=data)
        if honorserializer.is_valid():
            honorserializer.save()
        author = article.author_id
        noti_user = get_object_or_404(User, id=author)
        notification = {
                'nickname': noti_user.id,
                'message': 'MJ',
                'send_user': noti_user.id,
                'article_no': -1
            }
        json_noti = json.dumps(notification)
        noti_serializer = NotificationSerializer(data=json_noti)
        if noti_serializer.is_valid():
            noti_serializer.save()
        article.delete()
    return Response(serializer.data)


@api_view(['GET', ])
def honor(request):
    """
        명예의 전당에 올라있는 글 목록 노출 시 사용할 API

        ---
    """

    articles = HonorArticle.objects.all()
    datas = []
    for article in articles:
        article_serializer = HonorArticleSerializer(article)
        data = article_serializer.data
        for u in range(len(data['hashtags'])):
            hashtag = get_object_or_404(Hashtag, id=data['hashtags'][u])
            data['hashtags'][u] = hashtag.hashtag
        datas.append(data)
    return Response(datas)


@api_view(['POST', ])
def hashtag(request):
    """
        게시글의 해시태그 클릭 시 해당 해시태그가 달려있는 글 가져올 때 쓸 API

        ---
    """

    hashtag = request.data.get('hashtag')
    hashtag_id = Hashtag.objects.filter(hashtag=hashtag)
    start = int(request.data.get('start'))
    articles = hashtag_id[0].hashtag_articles.all()
    datas = []
    for article in articles[start:start+10]:
        like_users = []
        for like_user in article.like_users.all():
            like_users.append(like_user.id)
        hashtags_id = []
        hashtags = []
        for hashtag in article.hashtags.all():
            hashtags.append(hashtag.id)
            hashtags_id.append(hashtag.hashtag)
        a = article.image
        serializer = ArticleSerializer(article)
        data = serializer.data
        data['hashtags'] = hashtags_id
        user = get_object_or_404(User, id=data['author'])
        comments = article.comment_set.all()
        comments_list = []
        for comment in comments:
            comments_list.append(comment.comment)
        user_serializer = UserSerializer(user)
        data['user'] = user_serializer.data
        data['comments'] = comments_list
        datas.append(data)
    return Response(datas)


@api_view(['POST', ])
def keyword(request):
    """
        키워드 검색 시 해당 키워드와 일치하는 해시태그 가져올 때 사용하는 API

        ---
    """

    keyword = request.data.get('keyword')
    hashtags = Hashtag.objects.all()
    datas = []
    for hashtag in hashtags:
        if keyword in hashtag.hashtag:
            datas.append(hashtag.hashtag)
    return Response(datas)


@api_view(['GET', ])
def hashtagtrend(request):
    """
        많이 사용된 해시태그

        ---
    """
    hashtags = Hashtag.objects.all()
    datas = []    
    for hashtag in hashtags:
        datas.append([len(hashtag.hashtag_articles.all()), hashtag.hashtag])
        datas.sort(key=lambda x: x[0])
    return Response(datas)
        

@api_view(['GET', ])
def monthlytrend(request):
    """
        이전 한 달 간 인기글 가져올 때 사용할 API

        ---
    """
    hashtags = Hashtag.objects.all()
    articles = Article.objects.order_by('-popular_post', '-id')
    datas = []

    for article in articles:
        if article.popular_post == datetime.now().month:
            comments = article.comment_set.all()
            article_serializer = ArticleSerializer(article)
            account = get_object_or_404(User, id=article_serializer.data.get('author'))
            data = article_serializer.data
            data['pic_name'] = f'/uploads/{account.pic_name}'
            for u in range(len(data['hashtags'])):
                hashtag = get_object_or_404(Hashtag, id=data['hashtags'][u])
                data['hashtags'][u] = hashtag.hashtag
            data['nickname'] = account.nickname
            data['comments'] = len(comments)
            datas.append(data)
        if len(datas) == 10:
            break
    return Response(datas)
