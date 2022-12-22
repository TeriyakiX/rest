from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.response import Response
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
import rest_framework.permissions
from rest_framework.authtoken.models import Token

from .models import Book, Author, User
from .serializers import BookSerializer, AuthorSerializer, UserSerializer


class BookCreate(generics.ListCreateAPIView):

    queryset = Book.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookUpdate(generics.UpdateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    queryset = Book.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = BookSerializer


class AuthorCreate(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    queryset = Author.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = AuthorSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['author__name', 'title', 'genre']

    def get_queryset(self):
        return Book.objects.all()


def book_detail(request, pk):
    """
    Retrieve, update or delete a code book.
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        book.delete()
        return HttpResponse(status=204)


class author_list(generics.ListAPIView):
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Author.objects.all()


class AuthorDetail(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
