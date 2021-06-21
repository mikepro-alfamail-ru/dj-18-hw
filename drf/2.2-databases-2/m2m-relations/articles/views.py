from django.views.generic import ListView
from django.shortcuts import render

from articles.models import Article, ArticleTag


def articles_list(request):
    template = 'articles/news.html'
    ordering = '-published_at'
    articles = Article.objects.all().order_by(ordering)

    context = {'object_list': articles}
    for article in articles:
        print('-----')
        for scope in article.scopes.all():
            print(scope.__dict__)
    return render(request, template, context)