from django.db import models

# Create your models here.
# 分類, 選択肢
CATEGORY = (("business", "ビジネス"), ("life", "生活"), ("other", "その他"))


# 本クラス(モデル)
class Book(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY)

    # オブジェクトの文字列表現を返す特殊メソッド
    def __str__(self):
        return self.title
