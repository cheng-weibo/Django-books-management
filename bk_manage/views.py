from django.shortcuts import render, redirect
from bk_manage import models
from bk_manage.myForm import BookFrom, PublisherForm, AuthorForm
import json
from django.core import serializers
from django.db.utils import IntegrityError
from my_widgets.page import page
# Create your views here.


def index(request):
    books = models.Book.objects.all()
    page_range, current_page = page(books, request, 6)

    return render(request, 'index.html', locals())


def add_book(request):
    fm = BookFrom()
    if request.method == "POST":
        fm = BookFrom(request.POST)
        try:
            if fm.is_valid():
                data = fm.cleaned_data
                data["publisher_id"] = data["publisher"]
                author = data["authors"]
                del data["publisher"]
                del data["authors"]
                obj = models.Book.objects.create(**data)
                obj.authors.add(*author)
                return redirect('/')
        except IntegrityError:
            error_msg = '该图书已存在'
            return render(request, 'add_book.html', locals())

    return render(request, 'add_book.html', locals())


def edit_book(request, nid):

    fm = BookFrom()
    book_obj = models.Book.objects.filter(pk=nid)
    ret = serializers.serialize("json", book_obj)
    to = request.GET.get('to')
    if to:
        target = '/' + to + '/'
    else:
        target = '/'

    if request.method == "POST":
        fm = BookFrom(request.POST)
        try:
            if fm.is_valid():
                data = fm.cleaned_data
                data["publisher_id"] = data["publisher"]
                author = data["authors"]
                del data["publisher"]
                del data["authors"]
                book_obj.update(**data)
                author_int = []
                for i in author:
                    author_int.append(int(i))
                book_obj.first().authors.set(author_int)
                return redirect(target)
        except IntegrityError:
            error_msg = '该图书已存在'
            data_dict = {'fm': fm, "ret": json.dumps(ret), 'nid': nid, 'error_msg': error_msg, 'target': target}
            return render(request, "edit_book.html", data_dict)

    return render(request, "edit_book.html", {'fm': fm, "ret": json.dumps(ret), 'nid': nid, 'target': target})


def delete_book(request, nid):
    models.Book.objects.filter(bid=nid).delete()
    return redirect('/')


def add_publisher(request):
    to = request.GET.get('to')
    target = '/' + to + '/'
    fm = PublisherForm()
    if request.method == "POST":
        fm = PublisherForm(request.POST)
        try:
            if fm.is_valid():
                models.Publisher.objects.create(**fm.cleaned_data)
                if to:
                    return redirect(target)
                else:
                    return redirect('/')
        except IntegrityError:
            error_msg = '该出版社已存在'
            return render(request, "add_publisher.html", locals())
            
    return render(request, "add_publisher.html", locals())


def add_author(request):
    to = request.GET.get('to')
    target = '/' + to + '/'
    fm = AuthorForm()
    if request.method == "POST":
        fm = AuthorForm(request.POST)
        try:
            if fm.is_valid():
                models.Author.objects.create(**fm.cleaned_data)
                if to:
                    return redirect(target)
                else:
                    return redirect('/')
        except IntegrityError:
            error_msg = '该作者已存在'
            return render(request, "add_author.html", locals())
    return render(request, "add_author.html", locals())


def publisher(request):
    publisher_obj = models.Publisher.objects.all()
    page_range, current_page = page(publisher_obj, request, 6)
    return render(request, 'publisher.html', locals())


def author(request):
    author_obj = models.Author.objects.all()
    page_range, current_page = page(author_obj, request, 5)
    return render(request, "author.html", locals())


def del_author(request, nid):
    author_obj = models.Author.objects.filter(pk=nid)
    # 删除作者要把其对应的书也删掉
    book_list = author_obj.first().book2au.all()
    for book in book_list:
        print(book.bid, book.title)
        models.Book.objects.filter(pk=book.bid).delete()

    author_obj.delete()

    return redirect('/author/')


def del_publisher(request, nid):
    print('publisher  ', nid)
    models.Publisher.objects.filter(pk=nid).delete()
    return redirect('/publisher/')


def edit_publisher(request, nid):
    fm = PublisherForm()
    publisher_obj = models.Publisher.objects.filter(pk=nid)
    ret = serializers.serialize("json", publisher_obj)
    if request.method == "POST":
        fm = PublisherForm(request.POST)
        try:
            if fm.is_valid():
                data = fm.cleaned_data
                publisher_obj.update(**data)
                return redirect('/publisher/')
        except IntegrityError:
            error_msg = '该出版社已存在'
            data_dict = {'fm': fm, 'ret': json.dumps(ret), 'nid': nid, 'error_msg': error_msg}
            return render(request, 'edit_publisher.html', data_dict)

    return render(request, 'edit_publisher.html', {'fm': fm, 'ret': json.dumps(ret), 'nid': nid})


def edit_author(request, nid):
    fm = AuthorForm()
    author_obj = models.Author.objects.filter(pk=nid)
    ret = serializers.serialize("json", author_obj)
    if request.method == "POST":
        fm = AuthorForm(request.POST)
        try:
            if fm.is_valid():
                data = fm.cleaned_data
                author_obj.update(**data)
                return redirect('/author/')
        except IntegrityError:
            error_msg = '该作者已存在'
            data_dict = {'fm': fm, 'ret': json.dumps(ret), 'nid': nid, 'error_msg': error_msg}
            return render(request, 'edit_author.html', data_dict)

    return render(request, 'edit_author.html', {'fm': fm, 'ret': json.dumps(ret), 'nid': nid})


def publisher_book(request, nid):
    to = request.GET.get('to')
    if to:
        target = '/' + to + '/'
    else:
        target = '/'
    pub = models.Publisher.objects.get(pk=nid)
    book_obj_list = pub.book_set.all()
    return render(request, 'publisher_book.html', locals())


def author_book(request, nid):
    to = request.GET.get('to')
    if to:
        target = '/' + to + '/'
    else:
        target = '/'
    author_obj = models.Author.objects.get(pk=nid)
    book_obj_list = author_obj.book2au.all()
    return render(request, 'author_book.html', locals())
