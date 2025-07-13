from django.urls import path
from .views import ProductListView, ProductDetailView, SubmitReviewView,RegisterView,Logout
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('products/', ProductListView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    path('reviews/submit/', SubmitReviewView.as_view()),
    path('auth/token/', obtain_auth_token),
    path('auth/register/', RegisterView.as_view()),
    path('auth/logout/', Logout.as_view()),

]


