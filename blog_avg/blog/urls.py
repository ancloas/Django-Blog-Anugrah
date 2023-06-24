from django.urls import path
from blog.views import(
    create_blog_view,
    detail_blog_view,
    edit_blog_view,
    comment_submit
)

app_name= 'blog'

urlpatterns =[
    path('create/', create_blog_view, name='create'),
    path('<slug>/', detail_blog_view, name='detail'),
    path('<slug>/edit', edit_blog_view, name='edit'),
    path('<slug>/comment/submit/', comment_submit, name='comment_submit'),
]
