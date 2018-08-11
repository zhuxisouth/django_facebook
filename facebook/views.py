from django.shortcuts import render, redirect
from facebook.models import Article, Comment

# Create your views here.


count = 0


def play2(request):
    global count
    name = '남주희'
    age = 20
    count += 1

    diary = ['7월 20일 - 너무 덥다.', '7월 21일 - 내일도 덥다.',
             '7월 22일 - 시원하네.']

    if age > 19:
        status = '성인입니다.'
    else:
        status = '미성년입니다.'

    return render(request, 'play2.html', {'name': name,
                                          'count': count,
                                          'status': status,
                                          'diary': diary})


visits = 0

def event(request):
    global visits
    name = '남주희'
    age = 20
    visits += 1

    if age > 19:
        identity = '(성인)'
    else:
        identity = '(미성년자)'

    if visits == 7:
        result = '당첨!'
    else:
        result = '꽝...'
    return render(request, 'event.html', {'name': name,
                                          'identity': identity,
                                          'visits': visits,
                                          'result': result})



def play(request):
    return render(request, 'play.html')


def profile(request):
    return render(request, 'profile.html')


def fail(request):
    return render(request, 'fail.html')


def help(request):
    return render(request, 'help.html')

def warn(request):
    return render(request, 'warn.html')

def newsfeed(request):
    articles = Article.objects.all()

    for feed in articles:
        if len(feed.text) > 100:
            feed.text = feed.text[:100] + '...'

    return render(request, 'newsfeed.html', {'articles': articles})

def detail_feed(request, number):
    article = Article.objects.get(pk=number)

    if request.method == 'POST':
        Comment.objects.create(
            article=article,
            author=request.POST["nickname"],
            text=request.POST["reply"],
            password=request.POST["password"]
        )
    return render(request, 'detail_feed.html', {'feed': article})

def new_feed(request):
    if request.method == 'POST':
        if request.POST['author'] != '' and request.POST['title'] != '' and request.POST['content'] != '' and request.POST['password'] != '':
            new_article = Article.objects.create(
                author=request.POST['author'],
                title=request.POST['title'],
                text=request.POST['content'] + ' - 추신: 감사합니다.',
                password=request.POST['password']
        )

        return redirect(f'/feed/{ new_article.pk }')

    return render(request, 'new_feed.html')

def remove_feed(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST':
        if request.POST['password'] == article.password:
            article.delete()
            return redirect('/')

        else:
            return redirect('/fail/')

    return render(request, 'remove_feed.html', {'feed': article})
