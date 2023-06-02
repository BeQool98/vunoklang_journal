from .models import *
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

def paginator_page(request):
    BookDetailPost_list = BookDetailPost.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(BookDetailPost_list, 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return {'book_page': pages}

def latest_uploads():  
    try:      
        queryset2=BookDetailPost.objects.all().order_by('-created_on')[:6]
    except:
        queryset2 = BookDetailPost.objects.all()
    try:
        owner = Owner_Details.objects.get()
    except:
        owner = Owner_Details.objects.all()
    return queryset2, owner