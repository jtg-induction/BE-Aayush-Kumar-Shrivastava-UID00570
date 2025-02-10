from django.conf import settings
from django.db import models


class Project(models.Model):
    """
        Needed fields
        - members (m2m field to CustomUser; create through table and enforce unique constraint for user and project)
        - name (max_length=100)
        - max_members (positive int)
        - status (choice field integer type :- 0(To be started)/1(In progress)/2(Completed), with default value been 0)

        Add string representation for this model with project name.
    """
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ProjectMember',
        related_name='projects',
        verbose_name='Members'
    )
    name = models.CharField(max_length=100, verbose_name='Project Name')
    max_members = models.PositiveIntegerField(verbose_name='Max Members')
    STATUS_CHOICES = [
        (0, 'To be started'),
        (1, 'In progress'),
        (2, 'Completed'),
    ]
    status = models.IntegerField(
        choices=STATUS_CHOICES, default=0, verbose_name='Status'
    )

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    """
    Needed fields
    - project (fk to Project model)
    - member (fk to User model - use AUTH_USER_MODEL from settings)
    - Add unique constraints

    Add string representation for this model with project name and user email/first name.
    """
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, verbose_name='Project'
    )
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Member'
    )

    class Meta:
        unique_together = ('project', 'member')

    def __str__(self):
        return f'{self.project.name} - {self.member.email}'
