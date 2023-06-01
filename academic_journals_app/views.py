from typing import Any, Dict
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.contrib import messages
from . utils import *


# Create your views here.
'''
def login_user(request):
    return render(request, "index.html")
'''

def about_page(request):
    
    headers=AboutHeaders.objects.get()
    about_lists=AboutPage.objects.all()
    editorial_members=EditorialMembers.objects.all()
    queryset2, owner = latest_uploads()
    
    
    print("headers", headers.second_header)
    context={"headers":headers, 
             "about_lists":about_lists, 
             "editorial_members":editorial_members, "new_query":queryset2,"owner":owner}
    return render(request, "about_page.html", context)

def contact_message(request):
    
    
    if request.method == "GET":
        # return HttpResponse("this method is not allowed")
        return HttpResponseRedirect('/about')
    else:
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        
        try:
            new_message=ContactUs(name=name, email=email, subject=subject, messagename=message)
            new_message.save()
            messages.success(request, "Message sent successfully")
            return HttpResponseRedirect(reverse("about"))
        except:
            messages.error(request, "Failed to send Message")
            return HttpResponseRedirect(reverse("about"))
        
        print("this is the name", name,email,subject, message)
        return HttpResponseRedirect('/about')
        



class Home(ListView):
    model = BookDetailPost
    template_name= "book.html"

    def  get_context_data(self,*args, **kwargs):
        query, owner = latest_uploads()
        category = Category.objects.all()
        page_data = paginator_page(self.request)
        pages = page_data['book_page']

        context = super(Home, self).get_context_data(*args, **kwargs)
        context["category"] = category
        context["book_page"] = pages 
        context["new_query"] = query
        context["owner"]= owner
        return context




class BookDetail(DetailView):
    model = BookDetailPost
    # form_class = CommentForm
    template_name= "book-details.html"
    # fields = '__all__'

    def get_context_data(self, *args, **kwargs):
         query, owner = latest_uploads()  
         category = Category.objects.all()  
         user= self.request.user

         print('user:', user.username)
         comment_form = CommentForm()
         unique_comment = Comment.objects.filter(comment=self.get_object()).order_by('-date_created')
         context= super(BookDetail, self).get_context_data(*args,**kwargs)
         context["category"] = category
         context["comment_form" ] = comment_form
         context["new_query"] = query
         context["unique_comment"] = unique_comment
         context["owner"]= owner

         return context
    
    def post(self, request, *args, **kwargs):
      
        new_comment = Comment(description=request.POST.get('description'), comment=self.get_object(), name=request.POST.get('name'), email=request.POST.get('email'))
        new_comment.save()
        comment_email = Comment_Email(name=request.POST.get('name'), email=request.POST.get('email'))
        comment_email.save()
        return self.get(self, request, *args, **kwargs)



   
def download(self, document_id) :
        try:
            document = get_object_or_404(BookDetailPost, pk=document_id)
        except:
            messages.info(self, 'Document not found')
        response = HttpResponse(document.book, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{document.book.name}"'
        return response


def category_id(request, title):
    query, owner = latest_uploads()
    category = Category.objects.all()
    category_id = BookDetailPost.objects.filter(category=title)
    page_data = paginator_page(request)
    pages = page_data['book_page']

    context = { 'category_id': category_id, 'category': category, 'book_page': pages, 'owner': owner, 'new_query':query }
    
    return render(request, 'category-option-id.html', context)

def search(request):
    query, owner = latest_uploads()
    category = Category.objects.all()
    page_data = paginator_page(request)
    pages = page_data['book_page']

    if request.method == 'POST':
        page_data = paginator_page(request)
        pages = page_data['book_page']
        search = request.POST.get('search_btn')
        searched = BookDetailPost.objects.filter(title__contains=search)
        searched_author = BookDetailPost.objects.filter(author__contains=search)


        context = {
             'searched': searched,
             'searched_author': searched_author,
             'book_page': pages,
             'search': search,
             'category': category,
             'book_page': pages,
             'owner': owner, 
             'new_query':query
        }
        return render(request, 'search.html', context)

    else:
        query, owner = latest_uploads()
        page_data = paginator_page(request)
        pages = page_data['book_page']
         
        return render(request, 'search.html', {'category': category, 'book_page': pages,'owner': owner, 'new_query':query})

