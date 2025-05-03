# from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm

# Create your views here.


class SignupView(CreateView):
    model = User  # DBに保存するmodel
    form_class = SignupForm  # 入力フォームの指定
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("index")  # 処理成功時に遷移するURL
