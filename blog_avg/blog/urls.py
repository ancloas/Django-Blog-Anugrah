from django.urls import path
from blog.views import(
    create_blog_view,
    detail_blog_view,
    edit_blog_view,
    comment_submit,
    like_post,
    subscribe,
    get_author_info,
    approve_blog_post_view,
    in_review_blog_view
)

app_name= 'blog'

urlpatterns =[
    path('create/', create_blog_view, name='create'),
    path('subscribe/', subscribe, name='subscribe'),
    path('get_author_info/', get_author_info, name='get_author_info'),
    path('in_review_posts/', in_review_blog_view, name='in_review_posts'),


    path('<slug>/', detail_blog_view, name='detail'),
    path('<slug>/edit', edit_blog_view, name='edit'),
    path('<slug>/comment/submit/', comment_submit, name='comment_submit'),
    path('<slug>/like/', like_post, name='like_post'),
    path('<slug>/approve_blog_post/', approve_blog_post_view, name='approve_blog_post'),

]
