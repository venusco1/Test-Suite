from django.shortcuts import render

# Create your views here.


def editor_view(request):
    return render(request, "public/editor.html")
