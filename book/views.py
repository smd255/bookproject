from django.core.paginator import Paginator
from django.db.models import Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)

from .consts import ITEM_PER_RAGE
from .models import Book, Review


# Create your views here.


# index表示
def index_view(request):
    """
    Book.objects：Bookテーブルに格納されている全データ。
    (Model由来の)様々なメソッドを持つ。
    """
    # idで整列。"-"付与により降順。
    object_list = Book.objects.order_by("-id")

    # ランキング順。降順
    # アンダースコア2つで外部キーを参照
    ranking_list = Book.objects.annotate(avg_rating=Avg("review__rate")).order_by(
        "-avg_rating"
    )

    # ページネーション
    paginator = Paginator(ranking_list, ITEM_PER_RAGE)  # 必要な数に分割してobj取得
    page_number = request.GET.get("page", 1)  # URLからページ番号の取得。デフォルトは1
    page_obj = paginator.page(page_number)  #

    return render(
        request,
        "book/index.html",
        {
            "object_list": object_list,
            "ranking_list": ranking_list,
            "page_obj": page_obj,
        },
    )


# 本棚リスト表示
# 多重継承。左側が優先。ログイン関係は優先したいから左に記述。
class ListBookView(LoginRequiredMixin, ListView):
    """
    非ログイン状態ではViewを表示しない。
    ログイン後の遷移ページはsettings.pyでLOGIN_REDIRECT_URLにて設定済み。
    """

    template_name = "book/book_list.html"  # テンプレート設定
    model = Book  # 記憶モデル設定
    paginate_by = ITEM_PER_RAGE  # ページネーション設定


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

    # override
    # ユーザーIDを渡す
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# 削除用表示
class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = "book/book_confirm_delete.html"
    model = Book
    success_url = reverse_lazy("list-book")

    # override
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied

        return obj


# 編集用表示
class UpdateBookView(LoginRequiredMixin, UpdateView):
    template_name = "book/book_update.html"
    model = Book
    fields = ("title", "text", "category", "thumbnail")
    success_url = reverse_lazy("list-book")

    # override
    def get_object(self, queryset=None):
        # URLから指定のオブジェクトを取得
        obj = super().get_object(queryset)

        # オブジェクトのユーザーと現在のユーザーの判定
        if obj.user != self.request.user:
            # 403の例外
            raise PermissionDenied

        return obj


# レビュー作成用表示
class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ("book", "title", "text", "rate")
    template_name = "book/review_form.html"

    # override
    # viewのレンダリング時にコールされる
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Bookオブジェクトを"book"キー(辞書型)に登録
        context["book"] = Book.objects.get(pk=self.kwargs["book_id"])
        return context

    # override
    # form送信時にコールされる
    def form_valid(self, form):
        # フォームのインスタンス内のuserにデータ追加
        form.instance.user = self.request.user

        return super().form_valid(form)

    # override
    def get_success_url(self):
        return reverse("detail-book", kwargs={"pk": self.object.book.id})
