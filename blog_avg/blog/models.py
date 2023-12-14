from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from ckeditor.fields import RichTextField

# Create your models here.

def upload_location(instance, filename, **kwargs):
    file_path='blog/{author_id}/{title}-{filename}'.format(author_id=str(instance.author.id), title=str(instance.title), filename=str(filename))
    return file_path

class BlogPost(models.Model):
    title               = models.CharField(max_length=100, null=False, blank=False)
    body                = RichTextField(max_length=5000)    
    image               = models.ImageField(upload_to=upload_location, null=False, blank=False)    
    date_published      = models.DateTimeField(auto_now_add=True, verbose_name="date published")        
    date_updated        = models.DateTimeField(auto_now=True, verbose_name="date updated")        
    author              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug                = models.SlugField(blank=True, unique=True)
    read_count          = models.PositiveIntegerField(default=0)
    likes               = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)


    
    def __str__(self) -> str:
        return self.title
    
    def get_excerpt(self):
        return self.body[:100]


@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

def pre_save_blogpost_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.author.username+ "_" + instance.title)

pre_save.connect(pre_save_blogpost_receiver, sender=BlogPost)


class Comment(models.Model):
    # Comment fields
    content             = models.TextField()
    author              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at          = models.DateTimeField(auto_now_add=True)
    blog_post           = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Comment by {self.author} on {self.blog_post}'
    


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.TextField(null=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email