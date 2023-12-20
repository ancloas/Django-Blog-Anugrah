from django.urls import path
from blog.views import(
    create_blog_view,
    detail_blog_view,
    edit_blog_view,
    comment_submit,
    like_post,
    subscribe,
    get_author_info
)

app_name= 'blog'

urlpatterns =[
    path('create/', create_blog_view, name='create'),
    path('subscribe/', subscribe, name='subscribe'),
    path('get_author_info/', get_author_info, name='get_author_info'),
    path('<slug>/', detail_blog_view, name='detail'),
    path('<slug>/edit', edit_blog_view, name='edit'),
    path('<slug>/comment/submit/', comment_submit, name='comment_submit'),
    path('<slug>/like/', like_post, name='like_post'),
]
