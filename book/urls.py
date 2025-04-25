from django.urls import path
from . import views

urlpatterns = [
    path("book/", views.ListBookView.as_view()),
    # どのdetailなのか指定(PrimalyKey)
    path("book/<int:pk>/detail/", views.DetailBookView.as_view()),
]
