from django.urls import path
from .views import CategoryView,detailView,ColorDetailView,SearchView

urlpatterns = [
    path('/search',SearchView.as_view()),
    path('/category/<str:category_name>', CategoryView.as_view()),
    path('/<str:product_name>', detailView.as_view()),
    path('/<str:product_name>/<str:color_name>', ColorDetailView.as_view()),
]
