import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from main.forms import NewsForm
from main.models import News
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Menampilkan halaman utama daftar berita
@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        news_list = News.objects.all()
    else:
        news_list = News.objects.filter(user=request.user)
    
    context = {
        'npm' : '2406404913',
        'name': request.user.username,
        'class': 'PBP A',
        'news_list': news_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)

# Membuat models news baru
@login_required(login_url='/login')
def create_news(request):
    form = NewsForm(request.POST or None)
    
    if form.is_valid() and request.method == 'POST':
        news_entry = form.save(commit = False)
        news_entry.user = request.user
        news_entry.save()
        return redirect('main:show_main')
    
    context = {
        'form': form
    }
    
    return render(request, 'create_news.html', context)

# Menampilkan detail berita berdasarkan ID
def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()
    
    context = {
        'news': news
    }
    
    return render(request, 'news_detail.html', context)

# Menampilkan seluruh data dalam format XML
def show_xml(request):
    news_list = News.objects.all()
    xml_data = serializers.serialize("xml", news_list)
    return HttpResponse(xml_data, content_type="application/xml")

# Menampilkan seluruh data dalam format JSON
def show_json(request):
    news_list = News.objects.all()
    json_data = serializers.serialize("json", news_list)
    return HttpResponse(json_data, content_type="application/json")

# Menampilkan data dalam format XML berdasarkan ID
def show_xml_by_id(request, news_id):
   try:
       news_item = News.objects.filter(pk=news_id)
       xml_data = serializers.serialize("xml", news_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except News.DoesNotExist:
       return HttpResponse(status=404)

# Menampilkan data dalam format JSON berdasarkan ID
def show_json_by_id(request, news_id):
   try:
       news_item = News.objects.get(pk=news_id)
       json_data = serializers.serialize("json", [news_item])
       return HttpResponse(json_data, content_type="application/json")
   except News.DoesNotExist:
       return HttpResponse(status=404)
   
# Registrasi user baru
def register(request):
    form = UserCreationForm()
    
    if request.method == "POST":
        form =  UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been succesfully created')
            return redirect('main:login')   
         
    context = {
        'form': form
    }
    
    return render(request, 'register.html', context)

# Login User
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
    
        if form.is_valid():
            user = form.get_user()
            login(request, user)    # Disini session akan dibuat jika user berhasil login
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    
    else:
        form = AuthenticationForm(request)
    
    context = {'form': form}
    return render(request, 'login.html', context)

# Logout User
def logout_user(request):
    logout(request)  # Disini session akan dihapus saat user logout
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

# Mengedit berita berdasarkan ID
def edit_news(request, id):
    news = get_object_or_404(News, pk=id)
    form = NewsForm(request.POST or None, instance=news)
    
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')
    
    context = {
        'form': form,
    }
    
    return render(request, 'edit_news.html', context)
    
# Menghapus berita berdasarkan ID
def delete_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.delete()
    return HttpResponseRedirect(reverse('main:show_main'))