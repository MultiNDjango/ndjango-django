from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def homepage(request):

    # return render(request, 'book_rank_app/base.html', context)
    return render(request, 'homepage/index.html')


def contact(request):

    return render(request, 'homepage/contact.html')