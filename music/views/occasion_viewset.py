from rest_framework import viewsets
from ..models import Occasion
from ..serializers import OccasionSerializer


class OccasionViewSet(viewsets.ModelViewSet):
    queryset = Occasion.objects.all()
    serializer_class = OccasionSerializer