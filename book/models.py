from django.db import models
from .consts import MAX_RATE


# Create your models here.
# 分類, 選択肢
CATEGORY = (("business", "ビジネス"), ("life", "生活"), ("other", "その他"))

# ??
RATE_CHOICES = [(x, str(x)) for x in range(0, MAX_RATE + 1)]


# 書籍の内容
class Book(models.Model):
    title = models.CharField(max_length=100)  # タイトル
    text = models.TextField()  # 内容
    thumbnail = models.ImageField(null=True, blank=True)  # 画像表示
    category = models.CharField(max_length=100, choices=CATEGORY)  # カテゴリー

    # オブジェクトの文字列表現を返す特殊メソッド
    def __str__(self):
        return self.title


# レビュー内容
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Bookモデルの外部キー
    title = models.CharField(max_length=100)  # タイトル
    text = models.TextField()  # 詳細
    rate = models.IntegerField(choices=RATE_CHOICES)  # 評価
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)  # 作成者

    def __str__(self):
        return self.title
