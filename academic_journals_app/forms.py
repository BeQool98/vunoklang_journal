
from django import forms
from .models import *

#Building the comment form
class CommentForm(forms.ModelForm):
    class Meta:
        # verbose_name="Comment"
        # verbose_name_plural="Comment"
        model = Comment
        fields = ('name','email', 'description')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }
