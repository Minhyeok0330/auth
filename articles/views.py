from django.shortcuts import render, redirect
from .forms import ArticleForm
from .models import Article
from accounts.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)

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

def detail(request, id):
    article = Article.objects.get(id=id)
    context = {
        'article' : article
    }

    return render(request, 'detail.html', context)

def delete(request, id):
    article = Article.objects.get(id=id) 
    account = request.user
    if article.user_id == account.id:
        article.delete()
        return redirect('articles:index')
    else:
        return redirect('articles:detail', article.id)

def update(request, id):
    article = Article.objects.get(id=id) 
    account = request.user
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if article.user_id == account.id:
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.id)

        else:
            return redirect('articles:detail', article.id)
    else:
        form = ArticleForm(instance=article)
        context = {
            'form':form,
            'article' : article,
        }
        return render(request, 'update.html', context)
        
