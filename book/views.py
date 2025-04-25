from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book


# Create your views here.


# 本棚リスト表示
class ListBookView(ListView):
    template_name = "book/book_list.html"
    model = Book


class DetailBookView(DetailView):
    template_name = "book/book_detail.html"
    model = Book
