from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import ShareLink
from ..serializers import ShareLinkSerializer


class ShareLinkViewSet(viewsets.ModelViewSet):
    serializer_class = ShareLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShareLink.objects.filter(song__owner=self.request.user)