from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Book


# Create your views here.


# 本棚リスト表示
class ListBookView(ListView):
    template_name = "book/book_list.html"
    model = Book


class DetailBookView(DetailView):
    template_name = "book/book_detail.html"
    model = Book


class CreateBookView(CreateView):
    template_name = "book/book_create.html"
    model = Book
    fields = ("title", "text", "category")
    """
    通常のreverseではアプリ初期化段階で即時実行。アプリ初期化中なのでviewの名前が無くエラー。
    画面上でrequestが来た時に実行するためにlazyを使用。
    """
    success_url = reverse_lazy("list-book")
