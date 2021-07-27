# Create your views here.
from rest_framework import generics, mixins
from django.http import Http404

from rest_framework.response import Response
from .models import Operator, Aircraft, Manufacturer
from .serializers import (OperatorSerializer, AircraftSerializer, AircraftDetailSerializer, ManufacturerSerializer)

from django.utils.decorators import method_decorator
from pki_framework.utils import requires_scopes
# Create your views here.


@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class OperatorList(mixins.ListModelMixin,
                   generics.GenericAPIView):
    """
    List all operators, or create a new operator.
    """

    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class OperatorDetail(mixins.RetrieveModelMixin,
                               generics.GenericAPIView):
    """
    Retrieve, update or delete a Operator instance.
    """

    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class AircraftList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    """
    List all aircrafts in the database
    """

    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)





@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class AircraftDetail(mixins.RetrieveModelMixin,
        generics.GenericAPIView):
    """
    Retrieve, update or delete a Aircraft instance.
    """
    # authentication_classes = (SessionAuthentication,TokenAuthentication)
    # permission_classes = (IsAuthenticated,)

    queryset = Aircraft.objects.all()
    serializer_class = AircraftDetailSerializer
    
    def get_Aircraft(self, pk):
        try:
            a = Aircraft.objects.get(id=pk)
        except Aircraft.DoesNotExist:
            raise Http404
        else:
            return a

    def get(self, request, pk, format=None):
        aircraft = self.get_Aircraft(pk)
        serializer = AircraftDetailSerializer(aircraft)
        return Response(serializer.data)



@method_decorator(requires_scopes(['aerobridge.read']), name='dispatch')
class ManufacturerList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    """
    List all aircrafts in the database
    """

    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)





@method_decorator(requires_scopes(['aerobridge.read', 'aerobridge.write']), name='dispatch')
class ManufacturerDetail(mixins.RetrieveModelMixin,
        generics.GenericAPIView):
    """
    Retrieve, update or delete a Aircraft instance.
    """
    # authentication_classes = (SessionAuthentication,TokenAuthentication)
    # permission_classes = (IsAuthenticated,)

    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)