from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def user_profile(request):
    return Response({
        'username': request.user.username,
        'email': request.user.email,
    })
