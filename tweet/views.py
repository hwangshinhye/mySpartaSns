from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at')  # TweetModel에 저장한 모든 데이터를 불러옴(최신 역순)
            return render(request, 'tweet/home.html', {'tweet': all_tweet})  # 트윗 데이터를 변수에 담아 딕셔너리 형태로 돌려줌
        else:
            return redirect('/sign-in')
    elif request.method == 'POST':
        user = request.user  # 로그인 되어 있는 사용자의 정보 전체
        content = request.POST.get('my-content', '')
        tags = request.POST.get('tag', '').split(',')  # 웹 화면에서 장고 서버로 받아오는 태그 작성

        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')  # TweetModel에 저장한 모든 데이터를 불러옴(최신 역순)
            return render(request, 'tweet/home.html', {'error': '글은 공백일 수 없습니다'})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            # 해당하는 태그 목록 분리
            for tag in tags:
                tag = tag.strip()  # strip: 공백 제거
                if tag != '':
                    my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet')


@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')


# detail_tweet / write_comment / delete_comment

def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    # 댓글 모델 가져오기
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request, 'tweet/tweet_detail.html', {'tweet': my_tweet, 'comment': tweet_comment})


@login_required()
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()

    return redirect('/tweet/' + str(id))


def delete_comment(request, id):  # id는 comment의 id
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/' + str(current_tweet))


class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
