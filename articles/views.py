from django.shortcuts import render, redirect
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from accounts.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create(request):
    if request.method=='POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()
        context = {
            'form':form,
        }
    return render(request, 'create.html', context)

def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)

def detail(request, id):
    article = Article.objects.get(id=id)
    form = CommentForm()
    context = {
        'article': article,
        'form': form,
    }

    return render(request, 'detail.html', context)

@login_required
def delete(request, id):
    article = Article.objects.get(id=id) 

    if article.user == request.user:
        article.delete()

        return redirect('articles:index')

    else:
        return redirect('articles:detail', article.id)

@login_required
def update(request, id):
    article = Article.objects.get(id=id) 
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if article.user == request.user:
            if form.is_valid():
                form.save()

        return redirect('articles:detail', article.id)
    else:
        form = ArticleForm(instance=article)
        context = {
            'form':form,
        }
        return render(request, 'update.html', context)
        
@login_required
def comment_create(request, article_id):
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)

        # #객체를 저장하는 경우
        # comment.user = request.user
        # article = Article.objects.get(id=article_id)
        # comment.article = article

        #id값을 저장하는 경우
        comment.user_id = request.user.id
        comment.article_id = article_id

        comment.save()

        return redirect('articles:detail', id=article_id)

@login_required
def comment_delete(request, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.user:
        comment.delete()
    
    return redirect('articles:detail', id=article_id)