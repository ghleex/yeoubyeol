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
                hashtag, created = Hashtag.objects.get_or_create(hashtag=word)
                hash_serializer = HashtagSerializer(data=hashtag)
                if hash_serializer.is_valid():
                    hash_serializer.save()
                article.hashtags.add(hashtag)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class ArticleDetail(APIView):
    # 아래는 삭제 금지
    """
        작성한 글 내용을 받고, 삭제할 때 사용할 API

        ---
    """
    def get_object(self, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        return article

    # 글 상세보기
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

    # 글 삭제
    def delete(self, request, pk, format=None):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def update(request):
    # 아래는 삭제 금지
    """
        글 수정할 때 사용할 API

        ---
    """
    pk = request.data.get('id')
    article = get_object_or_404(Article, id=pk)
    article.article = request.data.get('article')
    article_hashtags = article.hashtags.all()
    for article_hashtag in article_hashtags:
        article.hashtags.remove(article_hashtag.id)
    if request.data.get('image'):
        article.image = request.data.get('image')
    hashtags = request.data.get('hashtags')
    hashtags = hashtags.split(',')
    # like_users = article.like_users.all()
    for word in hashtags:
        hashtag, created = Hashtag.objects.get_or_create(hashtag=word)
        hash_serializer = HashtagSerializer(data=hashtag)
        if hash_serializer.is_valid():
            hash_serializer.save()
        article.hashtags.add(hashtag)
    # for hashtag in hashtags: 

    data = {
        'article': article.article,
        'author': article.author_id,
        'image': article.image,
    }
    serializer = ArticleSerializer(article, data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(article.id)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    print(content)
    okt = Hannanum()
    print(content)
    keywords = okt.nouns(content)
    print(keywords)
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
    print('1111111111111111111')
    print(request.data)
    print(nickname)
    print('1111111111111111111')
    articles = Article.objects.filter(author=account.id)
    like_articles = Article.objects.all()
    print(articles)
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
    print(result)
    return Response(result)

 

# 유저 검색
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
                        'nickname': user.nickname,
                        'pic_name': f'/uploads/{user.pic_name}',
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
    """
        팔로우 신청할 때 사용할 API

        ---
    """
            
    # 팔로우 신청
    # @login_required
    def post(self, request, format=None):
        me = get_object_or_404(get_user_model(), nickname=request.data.get('my_nickname'))
        you = get_object_or_404(get_user_model(), nickname=request.data.get('your_nickname'))
        if me != you:
            # if serializer.data.followers.filter(pk=me.id).exists():
            if me in you.followers.all():
                you.followers.remove(me)
                # serializer.data.followers.remove(me.id)
            else:
                notification = {
                    'nickname': you.nickname,
                    'message': me.nickname + '님이 팔로우를 신청했습니다.',
                    'send_user': me.nickname
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
        다른 유저의 팔로잉하는 사람 목록 보기

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
        다른 유저의 팔로워 목록 보기

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
            # index = serializer.data.get('like_users').index(user.id)
            article.like_users.remove(user.id)
        else:
            article.like_users.add(user.id)
            like_users = article.like_users.all()
            for like_user in like_users:
                # 알림 받는 유저
                user  = get_object_or_404(User, username=like_user)
                receive_user = get_object_or_404(User, id=article.author_id)
                if user != receive_user:
                    notification = {
                        'nickname': receive_user.nickname,
                        'message': user.nickname + '님이' + receive_user.nickname + '님의 글을 좋아합니다.',
                        'send_user': user.nickname
                    }
                    noti_serializer = NotificationSerializer(data=notification)
                    if noti_serializer.is_valid():
                        notification = noti_serializer.save()
                        notification.save()
    if len(article.like_users.all()) >= 30000:
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
                'nickname': noti_user.nickname,
                'message': noti_user.nickname + '님의 글이 명예의 전당에 올라갔습니다.',
                'send_user': noti_user.nickname
            }
        json_noti = json.dumps(notification)
        noti_serializer = NotificationSerializer(data=json_noti)
        if noti_serializer.is_valid():
            noti_serializer.save()
        article.delete()
    return Response(serializer.data)


class CommentList(APIView):
    # 아래는 삭제 금지
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
        # request = my_nickname, article_author, comment
        article = self.get_object(request.data.get('article_id'))
        my_nickname = request.data.get('my_nickname')
        comment = request.data.get('comment')
        user = get_object_or_404(User, nickname=my_nickname)
        article_user = get_object_or_404(User, id=article.author_id)
        comment_data = {
            'article': article_id,
            'author': user.id,
            'comment': comment
        }
        serializer = CommentSerializer(data=comment_data)
        if article_user != user:
            notification = {
                    'nickname': article_user.nickname,
                    'message': user.nickname + '님이' + article_user.nickname + '님의 글에 댓글을 남겼습니다.',
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


class CommentDetail(APIView):
    # 아래는 삭제 금지
    """
        작성한 댓글을 수정하거나 삭제할 때 사용할 API

        ---
    """

    # 수정/삭제할 댓글 가져오기
    def get_object(self, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        return comment

    # 댓글 수정
    def put(self, request):
        # request = article_id, comment_id, comment
        comment = self.get_object(request.data.get('comment_id'))
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
        comment = self.get_object(pk)
        print(comment)
        comment.delete()
        return Response({'message': '댓글이 성공적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', ])
def honor(request):
    """
        명예의 전당에 올라있는 글 목록 노출 시 사용할 API

        ---
    """

    articles = HonorArticle.objects.all()
    serializer = HonorArticleSerializer(articles, many=True)
    return Response(serializer.data)


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
def trend(request):
    """
        이전 한 달 간 인기글 가져올 때 사용할 API

        ---
    """
    articles = Article.objects.all()
    print(articles)
    datas = []
    for article in articles:
        if article not in datas:
            serializer = ArticleSerializer(article)
            datas.append(serializer.data)
        if len(datas) == 10:
            break
    # .order_by('-like_users')
    return Response(datas)

        

