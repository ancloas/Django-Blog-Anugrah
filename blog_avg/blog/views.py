from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.db.models import Count


from blog.models import BlogPost, Comment
from blog.forms import CreateBlogPostForm, EditBlogPostForm
from account.models import Account



def create_blog_view(request):
    context= {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    
    form = CreateBlogPostForm(request.POST or None, request.FILES or None, )
    if form.is_valid():
        obj = form.save(commit=False)
        author= Account.objects.filter(email=user.email).first()
        obj.author=author
        obj.save()  
        form =  CreateBlogPostForm()
        context['is_saved']=True
        

    context['form'] =   form

    return render(request, 'blog/create_blog.html', context)



def detail_blog_view(request, slug):
    context ={}

    blog_post=get_object_or_404(BlogPost, slug = slug)
    comments = blog_post.comments.all()
    
	
	#increment the read count of the blog 
    blog_post.read_count+=1
    blog_post.save()
    

    context['blog_post']=blog_post
    context['comments']=comments
    
    
	#list all comments for the blog
	

    return render(request, 'blog/detail_blog.html', context)


def edit_blog_view(request, slug):
	
	context = {}
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if blog_post.author != user:
		return HttpResponse("You are not the author of the post")

	if request.POST:
		form = EditBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj
	
	form = EditBlogPostForm(
			initial={
					"title": blog_post.title, 
					"body": blog_post.body,
					"image": blog_post.image,
				}
			)
	context['form'] = form

	return render(request, 'blog/edit_blog.html', context)


def get_blog_queryset(query=None):
	queryset= []
	queries= query.split(" ")  
	for q in queries: 
		posts= BlogPost.objects.filter(Q(title__icontains=q) | Q(body__icontains=q)).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))
	

def get_popular_blogs():
    context ={}
    popular_posts = BlogPost.objects.annotate(num_reads=Count('read_count')).order_by('-read_count')[:4]
    print([post.title for post in popular_posts])
    return popular_posts



def comment_submit(request, slug):
    if request.method == 'POST':
        user = request.user
        if not user.is_authenticated:return redirect('must_authenticate')
        # Get the submitted comment data from the request
        comment_text = request.POST.get('comment_text')

        # Get the corresponding blog post
        blog_post=get_object_or_404(BlogPost, slug = slug)

        # Create a new comment object
        comment = Comment(blog_post=blog_post, content=comment_text, author=user)

        # Save the comment to the database
        comment.save()

    # Redirect the user back to the blog post
    return redirect('blog:detail', slug=blog_post.slug)	
    