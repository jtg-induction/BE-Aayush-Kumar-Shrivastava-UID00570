from rest_framework.viewsets import ModelViewSet

from todos import (
  models as todo_models,
  serializers as todo_serializers
)


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
        queryset = todo_models.Todo.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return todo_serializers.TodoAPICreateSerializer
        return todo_serializers.TodoAPIResponseSerializer
