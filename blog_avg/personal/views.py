from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
import requests
from dotenv import load_dotenv
import os

from blog.views import get_blog_queryset, get_popular_blogs, subscribe
from .mail_module import send_mail
from blog.forms import SubscriberForm

# Create your views here.
BLOG_POSTS_PER_PAGE=10

BODY_MESSAGE_FROM_USER = """  
        <div style="max-width: 600px; margin: 20px auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <p>Hello Bubble Of Thoughts,</p>
            <p>You got a new message from {0}:</p>
            <div style="border-left: 4px solid #007bff; padding: 12px; font-style: italic; margin-top: 20px;">
                <p style="margin: 0; padding: 0;">
                    {1}
                </p>
            </div>
            <p style="margin-top: 20px; font-style: italic; color: #555;">Best wishes,<br>{0}</p>
        </div>
    """
CONFIRM_MESSAGE_TEMPLATE_FROM_SERVER = """
<div style="max-width: 600px; margin: 20px auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <p>Hello {0},</p>
            <p>Your following message has been delivered to us, and we will soon respond.</p>
            <div style="border-left: 4px solid #007bff; padding: 12px; font-style: italic; margin-top: 20px;">
                <p style="margin: 0; padding: 0;">
                    {1}
                </p>
            </div>
            <p style="margin-top: 20px; font-style: italic; color: #555;">Best wishes,<br>Anugrah Gupta</p>
        </div>
"""

def home_screen_view(request, context={}):

    query =""
    
    if request.GET:
        query=request.GET.get('q','')
        context['query'] = str(query)


    blog_posts = sorted(get_blog_queryset(query, status='published'), key= attrgetter('date_published'), reverse=True)

    #get top most popular blogs
    popular_posts= get_popular_blogs(blog_posts)

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
    context['subscriber_form']=SubscriberForm()

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
        msg_body_from_user= BODY_MESSAGE_FROM_USER.format(template_params['from_name'], template_params['message'])
        msg_body_from_server= CONFIRM_MESSAGE_TEMPLATE_FROM_SERVER.format(template_params['from_name'], template_params['message'])

        # mail from user to my email
        result= send_mail(subject= 'Message from reader', msg_content=msg_body_from_user, from_name=template_params['from_name'], reply_to=template_params['reply_to'])
        # Send a Receipt mail to user
        result= send_mail(subject= 'We got your message', msg_content=msg_body_from_server, receiver=template_params['reply_to'], reply_to='bubbleofthought@outlook.com')

        # Check if the email was sent successfully
        if result:
            context['mail_status']='success'
        else:
            context['mail_status']='something went wrong, please check mail address again.'
    
        return render(request, 'personal/contact.html',context)

