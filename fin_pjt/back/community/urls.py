from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('articles/<int:community_pk>/reviews/',  views.create_review),
    path('articles/<int:community_pk>/reviews/<int:review_pk>/', views.delete_review),
    path('notice/', views.notice),
    path('notice/<int:pk>/', views.notice_detail),

]
