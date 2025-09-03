from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'npm' : '2406404913',
        'name': 'Zita Nayra Ardini',
        'class': 'PBP F'
    }

    return render(request, "main.html", context)