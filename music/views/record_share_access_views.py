from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models import ShareLink


class RecordShareAccessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, token):
        from ..models import SharedSongAccess
        share_link = get_object_or_404(ShareLink, token=token, is_active=True)
        SharedSongAccess.objects.get_or_create(user=request.user, share_link=share_link)
        return Response({'status': 'ok'})