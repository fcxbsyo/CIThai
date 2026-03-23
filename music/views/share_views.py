from rest_framework import viewsets
from ..models import ShareLink
from ..serializers import ShareLinkSerializer


class ShareLinkViewSet(viewsets.ModelViewSet):
    queryset = ShareLink.objects.all()
    serializer_class = ShareLinkSerializer