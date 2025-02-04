from django.db.models import Q  

from rest_framework.viewsets import ModelViewSet 

from .serializers import TodoAPICreateSerializer, TodoAPIResponseSerializer
from .models import Todo

class TodoAPIViewSet(ModelViewSet):
    """
       success response for create/update/get
       {
         "name": "",
         "done": true/false,
         "date_created": ""
       }


       success response for list
       [
         {
           "name": "",
           "done": true/false,
           "date_created": ""
         }
       ]
    """

    queryset = Todo.objects.all()
    serializer_class = TodoAPICreateSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        queryset = None
        if user_id is not None:
            queryset = Todo.objects.filter(user__id=user_id)
        else:
            queryset = Todo.objects.all()

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return TodoAPICreateSerializer
        return TodoAPIResponseSerializer
