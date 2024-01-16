from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Book
from .serializer import BookSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from keycloak import KeycloakOpenID
from keycloak.keycloak_openid import KeycloakOpenID
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.conf import settings
def main_page(request):
    return render(request, 'main_page.html')


# Configure Keycloak settings
keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080/auth", 
                                 realm_name="library-dev", 
                                 client_id="library-auth",
                                 client_secret_key="DgZhrz0er6DH5bsqdj4Lb9WGioHSVXHq")

def login(request):
    # Get the authorization URL
    auth_url = keycloak_openid.authorization_url(redirect_uri="http://0.0.0.0:8080/realms/library-dev/protocol/openid-connect/auth")

    # Redirect the user to the Keycloak login page
    return HttpResponseRedirect(auth_url)

def callback(request):
    code = request.GET.get('code')  # Extract the authorization code from the request
    keycloak_openid = KeycloakOpenID(server_url=settings.KEYCLOAK_SERVER_URL,
                                     client_id=settings.KEYCLOAK_CLIENT_ID,
                                     realm_name=settings.KEYCLOAK_REALM,
                                     client_secret_key=settings.KEYCLOAK_CLIENT_SECRET)
    
    # Get token information using the received code
    token = keycloak_openid.token(code, redirect_uri=settings.KEYCLOAK_REDIRECT_URI)
    
    # Perform further operations (e.g., store token information, authenticate user, etc.)
    # You can access token information like token['access_token'], token['refresh_token'], etc.
    
    return HttpResponse("Successfully authenticated!")


# Protected view with Keycloak authentication
@api_view(['GET'])
def protected_view(request):
    if keycloak_openid.userinfo(request.headers.get("Authorization")):
        # Access granted, you can implement your logic here
        return Response({"message": "Access granted"})
    else:
        return Response({"message": "Access denied"}, status=403)

# CRUD API views with Keycloak authentication
@api_view(['GET'])
def book_list(request):
    if keycloak_openid.userinfo(request.headers.get("Authorization")):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    else:
        return Response({"message": "Access denied"}, status=403)

@api_view(['POST'])
def create_book(request):
    if keycloak_openid.userinfo(request.headers.get("Authorization")):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    else:
        return Response({"message": "Access denied"}, status=403)

@api_view(['GET'])
def view_book(request, pk):
    if keycloak_openid.userinfo(request.headers.get("Authorization")):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    else:
        return Response({"message": "Access denied"}, status=403)

@api_view(['PUT'])
def update_book(request, pk):
    if keycloak_openid.userinfo(request.headers.get("Authorization")):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    else:
        return Response({"message": "Access denied"}, status=403)

@api_view(['DELETE'])
def delete_book(request, pk):
    if keycloak_openid.userinfo(request.headers.get("Authorization")):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=204)
    else:
        return Response({"message": "Access denied"}, status=403)
