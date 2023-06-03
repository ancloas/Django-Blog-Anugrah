from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from blog.views import get_blog_queryset, get_popular_blogs


# Create your views here.
BLOG_POSTS_PER_PAGE=10

def home_screen_view(request):
    context={}

    query =""
    
    if request.GET:
        query=request.GET.get('q','')
        context['query'] = str(query)


    blog_posts = sorted(get_blog_queryset(query), key= attrgetter('date_published'), reverse=True)

    #get top most popular blogs
    popular_posts= get_popular_blogs()

    #   Pagination
    page = request.GET.get('page', 1)
    blog_posts_paginator=Paginator(blog_posts, BLOG_POSTS_PER_PAGE)

    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)
        
    context['blog_posts']=blog_posts
    context['popular_posts']=popular_posts

    return render(request, 'personal/home.html',context)



def about_view(request):
    context={}
    return render(request, 'personal/about.html',context)



def contact_view(request):
    context={}
    return render(request, 'personal/contact.html',context)