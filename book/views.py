from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from .models import Book, Review


# Create your views here.


# index表示
def index_view(request):
    """
    Book.objects：Bookテーブルに格納されている全データ。
    (Model由来の)様々なメソッドを持つ。
    """
    object_list = Book.objects.order_by("category")
    return render(request, "book/index.html", {"object_list": object_list})


# 本棚リスト表示
# 多重継承。左側が優先。ログイン関係は優先したいから左に記述。
class ListBookView(LoginRequiredMixin, ListView):
    """
    非ログイン状態ではViewを表示しない。
    ログイン後の遷移ページはsettings.pyでLOGIN_REDIRECT_URLにて設定済み。
    """

    template_name = "book/book_list.html"
    model = Book


# 詳細表示
class DetailBookView(LoginRequiredMixin, DetailView):
    template_name = "book/book_detail.html"
    model = Book


# 新規作成用表示
class CreateBookView(LoginRequiredMixin, CreateView):
    template_name = "book/book_create.html"
    model = Book
    fields = ("title", "text", "category", "thumbnail")
    """
    通常のreverseではアプリ初期化段階で即時実行。アプリ初期化中なのでviewの名前が無くエラー。
    画面上でrequestが来た時に実行するためにlazyを使用。
    """
    success_url = reverse_lazy("list-book")


# 削除用表示
class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = "book/book_confirm_delete.html"
    model = Book
    success_url = reverse_lazy("list-book")


# 編集用表示
class UpdateBookView(LoginRequiredMixin, UpdateView):
    template_name = "book/book_update.html"
    model = Book
    fields = ("title", "text", "category", "thumbnail")
    success_url = reverse_lazy("list-book")


# レビュー作成用表示
class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ("book", "title", "text", "rate")
    template_name = "book/review_form.html"

    # CreateView定義の関数をオーバーライド
    # viewのレンダリング時にコールされる
    # **kwargs:キーワード引数。今回の場合が<int:book_id>が渡される
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Bookオブジェクトを"book"キー(辞書型)に登録
        context["book"] = Book.objects.get(pk=self.kwargs["book_id"])
        return context

    # CreateView定義の関数をオーバーライド
    # form送信時にコールされる
    def form_valid(self, form):
        # フォームのインスタンス内のuserにデータ追加
        form.instance.user = self.request.user

        return super().form_valid(form)

    # CreateView定義の関数をオーバーライド
    def get_success_url(self):
        return reverse("detail-book", kwargs={"pk": self.object.book.id})
