from django.shortcuts import render
from account.models import User
from django.utils import timezone
from JmApp.models import Item
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import *

def home(request):
    items=Item.objects.all().order_by('-clickCount')
    return render(request, 'home.html', {'items':items})

def detail(request, id):
    item=get_object_or_404(Item, pk=id)
    item.clickCount+=1
    item.save()
    return render(request, 'detail.html', {'item':item})

def create(request):
    if request.method == "POST":
        new_item=Item()
        new_item.title=request.POST['title']
        new_item.pub_date=timezone.datetime.now()
        new_item.body=request.POST['body']
        new_item.image=request.FILES['image']
        
        user_id=request.user.id
        user = User.objects.get(id=user_id)
        new_item.author=user
        new_item.save()
        return redirect('home')
    
    else:
        return render(request, 'new.html')

def edit(request, id):
    if request.method=="POST":
        edit_item=Item.objects.get(id=id)
        edit_item.title=request.POST['title']
        edit_item.body=request.POST['body']
        edit_item.save()
        return redirect('detail', edit_item.id)
    else:
        item=Item.objects.get(id=id)
        return render(request, 'edit.html', {'item':item})

def delete(request,id):
    delete_item=Item.objects.get(id=id)
    delete_item.delete()
    return redirect('home')


# ----- comment -----

def create_comment(request, item_id):
    if request.method == 'POST':
        comment=Comment()
        comment.blog=get_object_or_404(Item, pk=item_id)
        comment.writer=request.POST['writer']
        comment.content=request.POST['content']
        comment.save()
        return redirect('detail', item_id)

def update_comment(request, item_id, comment_id):
    if request.method =='POST':
        update_comment=get_object_or_404(Comment, pk=comment_id)
        update_comment.writer=request.POST['writer']
        update_comment.content=request.POST['content']
        update_comment.save()
        return redirect('detail', item_id)
    else:
        blog=get_object_or_404(Item, pk=item_id)
        comment=get_object_or_404(Comment, pk=comment_id)
        return render(request, 'edit_comment.html', {'blog':blog,'comment':comment})

def delete_comment(request, item_id, comment_id):
    my_comment=Comment.objects.get(pk=comment_id)
    my_comment.delete()
    return redirect('detail', item_id)

# ----- search -----
def search(request):
    products = Item.objects.all()
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    search_word = request.POST.get('search_word')
    if search_word:
        products = products.filter(title__icontains = search_word)
        return render(request, 'productList.html', {'products':products, 'search_word':search_word})
    return render(request, 'productList.html', {'products':page, 'search_word':search_word})

def mypage(request, username):
    user = User.objects.filter(username=username)
    products = Item.objects.filter(author=user[0])
    if products is None:
        productsCount = 0
    else: productsCount = len(products)
    return render(request, 'myPage.html', {'products':products, 'users':user, 'productsCount':productsCount})
