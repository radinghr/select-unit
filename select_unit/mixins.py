from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import generics


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class GeneralClassMixin(generics.GenericAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
