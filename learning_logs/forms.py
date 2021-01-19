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
        labels = {'text': 'Создайте запись'}
        widgets = {'text': forms.Textarea(attrs={'cols': 500, 'placeholder': 'Введите текст'})}


class EditForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Редактируйте запись'}
        widgets = {'text': forms.Textarea(attrs={'cols': 500, 'placeholder': 'Введите текст'})}
