from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from main.forms import NewsForm
from main.models import News

# Create your views here.
def show_main(request):
    news_list = News.objects.all()
    
    context = {
        'npm' : '2406404913',
        'name': 'Zita Nayra Ardini',
        'class': 'PBP F',
        'news_list': news_list
    }

    return render(request, "main.html", context)

def create_news(request):
    form = NewsForm(request.POST or None)
    
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('show_main')
    
    context = {
        'form': form
    }
    
    return render(request, 'create_news.html', context)

def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()
    
    context = {
        'news': news
    }
    
    return render(request, 'news_detail.html', context)

def show_xml(request):
    news_list = News.objects.all()
    xml_data = serializers.serialize("xml", news_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    news_list = News.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")