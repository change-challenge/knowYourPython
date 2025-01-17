from django.urls import path

from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('question/create/', views.question_create, name='question_create'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('upload_to_s3/', views.upload_to_s3, name='upload_to_s3'),
    path('s3-presigned-url/', views.PresignedURLView.as_view(), name='presigned_url'),
]