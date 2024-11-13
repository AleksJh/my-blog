from .models import Comment
from django import forms

class EmailPostForm(forms.Form):
    '''
    A form for sending an email to share a blog post.

    Includes fields for the sender's name, email, recipient's email,
    and optional comments.
    '''
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,  # The field is optional.
                               widget=forms.Textarea)  # Displays the field as a multi-line text input.


class CommentForm(forms.ModelForm):
    '''
    A form for submitting comments linked to a specific blog post.

    Inherits from Django's ModelForm to create form fields based on the
    Comment model.
    '''
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

