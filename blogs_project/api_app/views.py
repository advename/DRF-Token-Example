from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView  # APIView class
# used to overwrite global API access permission
from rest_framework.permissions import AllowAny
from rest_framework.response import Response  # allow to send response
from rest_framework import status  # used to return status code
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from django.middleware.csrf import get_token
# Login View


# @method_decorator(ensure_csrf_cookie, name="post")
class Login(APIView):
    # set custom permission class for this view and overwrite the global default
    permission_classes = [AllowAny]

    # POST request
    def post(self, request, format=None):

        # Strip the username and password out of the json body (Should be done with a serializer?)
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user:
            # User authenticated, get the users token and return it
            csrf_token = get_token(request)
            token = user.auth_token.key

            # Respond with CSRF in body
            response = Response(
                {"message": "Successfully authenticated", "csrf": csrf_token})

            # Add the cookie with the token to the Response
            response.set_cookie("token", token, samesite=None,
                                httponly=True)
            return response

        else:
            # User not authenticated, return error
            return Response({"error": "Wrong credentials"}, status=status.HTTP_404_NOT_FOUND)
