from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound

from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import Http404

# Здесь представлены представления


def index(request):
    """Домашняя страница приложения learning_log"""
    return render(request, 'learning_logs/index.html')


def check_topic_owner(topic, request):
    """Проверка того, что тема принадлежит текущему пользователю"""
    if topic.owner != request.user:
        raise Http404


@login_required
def topics(request):
    """выводит список тем"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """выводит одну тему и все ее записи"""
    topic = Topic.objects.get(id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю
    # if topic.owner != request.user:
    #     raise Http404
    check_topic_owner(topic, request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """определяет новую тему"""
    if request.method != 'POST':
        #данные не отправлялись; создается пустая форма.
        form = TopicForm()
    else:
        #отправлены данные POST; обработать данные.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    #вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """добавляет новую запись по конкретной теме"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        #данные не отправлялиссь, создается пустая форма
        form = EntryForm()
    else:
        #данные отправлены, обработать данные
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return redirect('learning_logs:topic',topic_id=topic_id)

    #вывести пустую или недействительную форму
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """редактирует существующую запись"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    # Проверка того, что тема принадлежит текущему пользователю
    check_topic_owner(topic, request)

    if request.method != 'POST':
        #Исходный запрос; форма заполняется данными текущей запсиси.
        form = EntryForm(instance=entry)
    else:
        #отправка данных POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def delete_topic(request, topic_id):
    """удаляет тему"""
    try:
        topic = Topic.objects.get(id=topic_id)
        context = {'topic': topic}
        topic.delete()
        return HttpResponseRedirect("/topics")
    except Topic.DoesNotExist:
        return HttpResponseNotFound("<h2>Тема не найдена</h2>")


def delete_entry(request, entry_id):
    """удаляет запись"""
    try:
        entry = Entry.objects.get(id=entry_id)
        topic = entry.topic
        context = {'entry': entry}
        entry.delete()
        return redirect('learning_logs:topic', topic_id=topic.id)
    except Topic.DoesNotExist:
        return HttpResponseNotFound("<h2>Запись не найдена</h2>")
