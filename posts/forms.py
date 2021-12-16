from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('image', 'post_caption')
		

class EditPostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('post_caption',)

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('content',)
		widgets = {
			"content":forms.Textarea(attrs={"class": "form-control col-md-4",
			"placeholder": "Send a comment...",
			"rows": 2,
			"cols":50})
		}


class ReplyForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('content',)
		widgets = {
			"content":forms.Textarea(attrs={"class": "form-control col-md-4",
			"placeholder": "Send a reply...",
			"rows":2,
        	"cols":50})
		}