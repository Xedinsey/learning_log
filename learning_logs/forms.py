from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Создайте запись и добавьте ее'}
        widgets = {'text': forms.Textarea(attrs={'cols': 500, 'placeholder': 'Введите текст'})}
