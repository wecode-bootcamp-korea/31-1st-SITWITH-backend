from django.urls import path
from .views import DetailView,ProductListView

urlpatterns = [
    path('',ProductListView.as_view()),
    path('/<int:product_id>', DetailView.as_view())
]
