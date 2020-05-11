from django import forms
from django.forms import ModelForm, Textarea
from .models import Post, Group, Comment

def text_validator(value):
    if len(value) == 0:
        raise forms.ValidationError(
            'Это поле должно быть заполнено!',
            params={'value' : value},
        )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']
        fields_required = ['text']
        widgets = {
            'text' : Textarea
        }
        labels = {
            'group' : 'Выберите группу',
            'text' : 'Введите текст записи'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text' : Textarea
        }
