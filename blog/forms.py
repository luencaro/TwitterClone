from django import forms
from .models import Comment


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content']
        widgets = {
            'comment_content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Añade un comentario...'})
        }
