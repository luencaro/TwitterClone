from django import forms
from .models import Comment, Post


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content']
        widgets = {
            'comment_content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Añade un comentario...'})
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_content', 'image']
        widgets = {
            'post_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '¿Qué está pasando?'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            })
        }
        labels = {
            'post_content': 'Contenido',
            'image': 'Imagen (opcional)'
        }
