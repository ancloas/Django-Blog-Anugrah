from django import forms 
from ckeditor.widgets import CKEditorWidget

from blog.models import BlogPost, Comment, Subscriber


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model   = BlogPost
        fields = ['title', 'body', 'image', 'status']
    DRAFT = 'draft'
    IN_REVIEW = 'in_review'

    STATUS_CHOICES = [
       (DRAFT, 'Draft'),
        (IN_REVIEW, 'In Review'),
    ]
    body = forms.CharField(widget=CKEditorWidget(config_name='blog'))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.HiddenInput(), initial=DRAFT)



class EditBlogPostForm(forms.ModelForm):
    class Meta:
        model   = BlogPost
        fields  = ['title', 'body', 'image']
    DRAFT = 'draft'
    IN_REVIEW = 'in_review'

    STATUS_CHOICES = [
       (DRAFT, 'Draft'),
        (IN_REVIEW, 'In Review'),
    ]
    
    body = forms.CharField(widget=CKEditorWidget(config_name='blog'))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.HiddenInput(), initial=DRAFT)


    def save(self, commit=True): 
        blog_post=self.instance
        blog_post.title=self.cleaned_data['title']
        blog_post.body=self.cleaned_data['body']
        blog_post.status = self.cleaned_data['status']

        if self.cleaned_data['image']:
            blog_post.image=self.cleaned_data['image']

        if commit:
            blog_post.save()
        return blog_post



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email', 'name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'name-input', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'email-input', 'placeholder': 'Enter your email'}),
        }

