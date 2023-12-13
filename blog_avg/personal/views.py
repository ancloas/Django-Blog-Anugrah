from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
import requests
from dotenv import load_dotenv
import os

from blog.views import get_blog_queryset, get_popular_blogs
from .mail_module import send_mail

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


def send_email(request):
    context={}

    if request.method == 'POST':
        load_dotenv()

        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Prepare data for Email.js template
        template_params = {
            'from_name': name,
            'reply_to': email,
            'message': message,
        }

        result= send_mail(subject= 'Message from reader', msg_content=template_params['message'], from_name=template_params['from_name'], reply_to=template_params['reply_to'])
        # Make a request to Email.js
        
        # Check if the email was sent successfully
        if result:
            context['mail_status']='success'
        else:
            context['mail_status']='something went wrong, please check mail address again.'
    
        return render(request, 'personal/contact.html',context)

