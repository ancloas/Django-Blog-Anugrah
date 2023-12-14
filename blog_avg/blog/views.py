from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.db.models import Count
from django.http import JsonResponse
import logging


from blog.models import BlogPost, Comment, Subscriber
from blog.forms import CreateBlogPostForm, EditBlogPostForm, SubscriberForm
from account.models import Account
from django.contrib import messages
from personal.mail_module import send_mail
 

logger = logging.getLogger(__name__)

WELCOME_EMAIL_TEMPLATE = """  
    <div style="max-width: 600px; margin: 20px auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
        <p>Hello {0},</p>
        <p>Welcome to Bubble Of Thoughts! We are thrilled to have you as a subscriber to our newsletter.</p>
        <p>Stay tuned for exciting updates, interesting articles, and much more. Feel free to reach out to us anytime.</p>
        <div style="border-left: 4px solid #007bff; padding: 12px; font-style: italic; margin-top: 20px;">
            <p style="margin: 0; padding: 0;">
                If you have any questions or suggestions, don't hesitate to contact us.
            </p>
        </div>
        <p style="margin-top: 20px; font-style: italic; color: #555;">Best wishes,<br>Anugrah Gupta</p>
    </div>
"""
WELCOME_EMAIL_SUBJECT = 'Welcome to Bubble of Thoughts'
def create_blog_view(request):
    context= {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    if not user.is_writer:
        dict={"rwsponse": "User must be a writer"}
        return JsonResponse(data=dict)
    
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
    likes_count = blog_post.likes.count()
    liked_users = blog_post.likes.all()
    
	
	#increment the read count of the blog 
    blog_post.read_count+=1
    blog_post.save()
    

    context['blog_post']=blog_post
    context['comments']=comments
    context['likes_count']= likes_count
    context['liked_users']= liked_users
    context['subscriber_form']=SubscriberForm()
    
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
        if not user.is_authenticated:
            return redirect('must_authenticate')
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
    


def like_post(request, slug):
    if request.method == 'POST':
        user = request.user
        # not working as the parent function is called in a function in js. so not able to get the must authenticate
        if not user.is_authenticated:
            return redirect('must_authenticate')
        post = get_object_or_404(BlogPost, slug = slug)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        print(liked)


        return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})
   

def subscribe(request):
    response_data = {'success': False, 'message': 'Invalid request'}

    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        is_form_valid = True

        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                name = form.cleaned_data.get('name', '')  # Handle the case where name is not provided
                is_form_valid = True
                form.save()
                response_data['success'] = True
                response_data['message'] = 'You have successfully subscribed!'
                # Use logging instead of print for structured logging
                logger.info(f'Successful subscription for {email}')
                # Ensure that your email template has a placeholder for the name
                first_name= name.split(' ')[0]
                msg = WELCOME_EMAIL_TEMPLATE.format(first_name)
                print(msg)
                send_mail(subject=WELCOME_EMAIL_SUBJECT, msg_content=msg, receiver=email)
            except:
                response_data['success'] = False
                response_data['message'] = 'Something went wrong'
        else:
            error_lists=[]
            for field, errors in form.errors.items():
                error_lists.extend(errors)
            response_data['errors']=error_lists
            response_data['message'] = 'Invalid Input'


    logger.debug(f'Called subscribe: {response_data}, is_form_valid={is_form_valid}')
    return JsonResponse(response_data)
