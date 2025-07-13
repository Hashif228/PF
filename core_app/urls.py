from django.urls import path
from .views import ProductList, ProductDetail, SubmitReview,Register,Logout
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<int:pk>/', ProductDetail.as_view()),
    path('reviews/submit/', SubmitReview.as_view()),
    path('auth/token/', obtain_auth_token),
    path('auth/register/', Register.as_view()),
    path('auth/logout/', Logout.as_view())

]


