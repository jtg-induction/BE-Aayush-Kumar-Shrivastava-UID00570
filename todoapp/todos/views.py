from rest_framework.viewsets import ModelViewSet

from .models import Todo
from .serializers import TodoAPICreateSerializer, TodoAPIResponseSerializer


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

    def get_queryset(self):
        user = self.request.user
        queryset = None
        if user is not None:
            queryset = Todo.objects.filter(user_id=user.id)

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return TodoAPICreateSerializer
        return TodoAPIResponseSerializer
