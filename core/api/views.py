from .serializers import TodoListSerializer
# from rest_framework.views.generic import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import TodoList
from datetime import date
from django.contrib.auth.models import User


class TODO(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        day, month, yr = [int(x) for x  in data.get('date_created').split('-')]
        dt = date(yr, month, day)
        # res = TodoList.objects.filter(user__username=data.get('user')).order_by('-date_created')
        res = TodoList.objects.filter(user__username=data.get('user'), date_created__contains=dt).order_by('-date_created')
        # res = TodoList.objects.filter(date_created=dt).order_by('-date_created')
        print(res)
        seriaizer =  TodoListSerializer(res, many=True)
        return Response({'data': seriaizer.data})
        
