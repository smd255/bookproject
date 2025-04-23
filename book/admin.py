from django.contrib import admin
from .models import SampleModel

# Register your models here.
# データベーステーブルを管理画面に表示
admin.site.register(SampleModel)
