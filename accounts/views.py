
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.get_username(),
            "groups": list(request.user.groups.values_list("name", flat=True)),
            "is_staff": request.user.is_staff,
            "is_superuser": request.user.is_superuser,
        })
