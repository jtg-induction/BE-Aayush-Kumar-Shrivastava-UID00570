from django.urls import path
from projects import views as project_views

from rest_framework import routers

urlpatterns = [
    path('projects/<int:pk>/add/', project_views.ProjectMemberApiViewSet.as_view(
        {'patch': 'partial_update'}
    ), name='project-add'),
    path('projects/<int:pk>/remove/', project_views.ProjectMemberApiViewSet.as_view(
        {'patch': 'partial_update'}
    ), name='project-remove'),
]

router = routers.SimpleRouter()

router.register(r'projects', project_views.ProjectMemberApiViewSet, 'project')

urlpatterns += router.urls
