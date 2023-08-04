from django.urls import path
from .views import HomeView, BlogListView, BlogCreateView, BlogEditView, SignUpView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('blog/', BlogListView.as_view(), name='blogs'),
    path('blog/create', BlogCreateView.as_view(), name = 'create'),
    path('blog/edit/<int:pk>/', BlogEditView.as_view(), name='edit-blog'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
]
