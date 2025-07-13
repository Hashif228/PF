from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import NotFound

from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer, RegisterSerializer


class ProductList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        products = Product.objects.all()
        for product in products:
            reviews = Review.objects.filter(product=product)
            if reviews.exists():
                avg = sum([r.rating for r in reviews]) / len(reviews)
                product.average_rating = round(avg, 2)
            else:
                product.average_rating = None

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Only admins can add products."}, status=403)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProductDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound("Product not found")

    def get(self, request, pk):
        product = self.get_product(pk)
        reviews = Review.objects.filter(product=product)
        if reviews.exists():
            avg = sum([r.rating for r in reviews]) / len(reviews)
            product.average_rating = round(avg, 2)
        else:
            product.average_rating = None

        serializer = ProductSerializer(product)
        return Response(serializer.data)
    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admins can delete products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        product = self.get_product(pk)
        product.delete()
        return Response(
            {"message": "Product deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({"detail": "Only admins can update products."}, status=403)

        product = self.get_product(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class SubmitReview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get('product')

        if Review.objects.filter(user=user, product_id=product_id).exists():
            return Response(
                {"error": "You have already reviewed this product."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Register(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            return Response({"detail": "Token not found or already deleted."}, status=400)

        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
