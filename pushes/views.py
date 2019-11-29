from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from pywebpush import WebPushException
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Subscription
from .serializers import SubscriptionSerializer, PushMessageSerializer
from .utils import send_push


class PushesIndexView(TemplateView):
    template_name = 'pushes/pushes.html'


class SWView(TemplateView):
    template_name = 'pushes/sw.js'
    content_type='application/x-javascript'


class SubscribeView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer


class UnSubscribeView(APIView):

    def delete(self, request):
        data=request.data
        sub = get_object_or_404(Subscription, **data)
        sub.delete()
        return Response({'status': 'Subscribe is deleted'}, status=status.HTTP_204_NO_CONTENT)


class SendPushView(APIView):
    
    def post(self, request):
        message = PushMessageSerializer(data=request.data.get('message'))
        message.is_valid(raise_exception=True)
        sub = get_object_or_404(Subscription, subscription=request.data.get('subscription'))
        try:
            response = send_push(sub, message.validated_data)
        except WebPushException as exc:
            if exc.response.status_code == 410:
                sub.delete()
            return Response(
                {'status': 'fail', 'response': 'subscription is not registered'}, 
                status=status.HTTP_400_BAD_REQUEST,
            )
        if response.status_code >= 400:
            return Response(
                {'status': 'fail', 'response': response.status_code}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'status': 'successful'}, status=status.HTTP_200_OK)
